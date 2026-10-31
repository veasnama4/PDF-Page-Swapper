# -*- coding: utf-8 -*-
"""
PDF Page Swapper
Batch-swap adjacent PDF pages: 1<->2, 3<->4, ...
Designed for Python 3.8.10 and Windows 7 SP1 or newer.
"""
import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    from pypdf import PdfReader, PdfWriter
except Exception as exc:
    PdfReader = PdfWriter = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None

APP_NAME = "PDF Page Swapper"


def resource_path(relative_path):
    """Get resource path for PyInstaller or normal Python execution."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def output_path_for(source, output_dir):
    stem = os.path.splitext(os.path.basename(source))[0]
    candidate = os.path.join(output_dir, stem + "_swapped_pairs.pdf")
    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(
            output_dir, "{}_swapped_pairs_{}.pdf".format(stem, counter)
        )
        counter += 1
    return candidate


def swap_pdf_pages(source, destination):
    reader = PdfReader(source, strict=False)
    if reader.is_encrypted:
        try:
            result = reader.decrypt("")
            if not result:
                raise ValueError("This PDF is password-protected.")
        except Exception:
            raise ValueError("This PDF is password-protected.")

    writer = PdfWriter()
    page_count = len(reader.pages)

    # Add pages in adjacent pairs. If the page count is odd, keep the last page.
    order = []
    for index in range(0, page_count - 1, 2):
        order.extend([index + 1, index])
    if page_count % 2:
        order.append(page_count - 1)

    for index in order:
        writer.add_page(reader.pages[index])

    # Keep document metadata where available.
    try:
        if reader.metadata:
            metadata = {}
            for key, value in reader.metadata.items():
                if value is not None:
                    metadata[str(key)] = str(value)
            if metadata:
                writer.add_metadata(metadata)
    except Exception:
        pass

    with open(destination, "wb") as output_file:
        writer.write(output_file)

    return page_count


class PDFPageSwapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        try:
            self.root.iconbitmap(resource_path("pdf_page_swapper.ico"))
        except Exception:
            pass
        self.root.geometry("780x560")
        self.root.minsize(680, 480)
        self.files = []
        self.output_dir = ""
        self.is_processing = False

        self._configure_style()
        self._build_ui()

    def _configure_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Info.TLabel", font=("Segoe UI", 10))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=7)

    def _build_ui(self):
        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill="both", expand=True)

        ttk.Label(
            outer, text="PDF Page Swapper", style="Title.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            outer,
            text="ប្ដូរទំព័រ PDF ជាគូៗ៖ 1 ↔ 2, 3 ↔ 4, 5 ↔ 6 ...",
            style="Info.TLabel",
        ).pack(anchor="w", pady=(4, 12))

        file_bar = ttk.Frame(outer)
        file_bar.pack(fill="x", pady=(0, 6))
        ttk.Label(file_bar, text="ឯកសារ PDF ដែលបានជ្រើសរើស").pack(side="left")
        ttk.Button(
            file_bar, text="បន្ថែម PDF...", command=self.add_files
        ).pack(side="right")
        ttk.Button(
            file_bar, text="លុបបញ្ជី", command=self.clear_files
        ).pack(side="right", padx=6)

        list_frame = ttk.Frame(outer)
        list_frame.pack(fill="both", expand=True)
        self.file_list = tk.Listbox(
            list_frame, selectmode=tk.EXTENDED, font=("Segoe UI", 10),
            activestyle="dotbox"
        )
        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=scroll.set)
        self.file_list.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        output_frame = ttk.LabelFrame(outer, text="ទីតាំងរក្សាទុកឯកសារថ្មី", padding=10)
        output_frame.pack(fill="x", pady=(12, 8))
        self.output_var = tk.StringVar(value="ដាក់ឯកសារថ្មីនៅជាមួយឯកសារដើម")
        ttk.Label(output_frame, textvariable=self.output_var).pack(side="left", fill="x", expand=True)
        ttk.Button(output_frame, text="ជ្រើសរើស Folder...", command=self.choose_output).pack(side="right")

        note = (
            "ចំណាំ៖ ឯកសារដើមមិនត្រូវបានកែប្រែទេ។ ប្រសិនបើមានចំនួនទំព័រសេស "
            "ទំព័រចុងក្រោយនឹងនៅដដែល។"
        )
        ttk.Label(outer, text=note, wraplength=730, style="Info.TLabel").pack(anchor="w", pady=(2, 8))

        self.progress = ttk.Progressbar(outer, mode="determinate")
        self.progress.pack(fill="x", pady=(2, 8))
        self.status_var = tk.StringVar(value="ត្រៀមរួចរាល់")
        ttk.Label(outer, textvariable=self.status_var).pack(anchor="w")

        bottom = ttk.Frame(outer)
        bottom.pack(fill="x", pady=(12, 0))
        ttk.Button(bottom, text="ចាប់ផ្ដើមប្ដូរទំព័រ", style="Action.TButton",
                   command=self.start_processing).pack(side="right")
        ttk.Button(bottom, text="បិទកម្មវិធី", command=self.root.destroy).pack(side="right", padx=8)

    def add_files(self):
        paths = filedialog.askopenfilenames(
            title="ជ្រើសរើសឯកសារ PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        existing = set(self.files)
        for path in paths:
            if path.lower().endswith(".pdf") and path not in existing:
                self.files.append(path)
                self.file_list.insert(tk.END, path)
                existing.add(path)
        if self.files and not self.output_dir:
            self.output_var.set("ដាក់ឯកសារថ្មីនៅជាមួយឯកសារដើម")

    def clear_files(self):
        if self.is_processing:
            return
        self.files = []
        self.file_list.delete(0, tk.END)
        self.status_var.set("បានលុបបញ្ជីឯកសារ")

    def choose_output(self):
        folder = filedialog.askdirectory(title="ជ្រើសរើស Folder រក្សាទុក")
        if folder:
            self.output_dir = folder
            self.output_var.set(folder)

    def start_processing(self):
        if self.is_processing:
            return
        if PdfReader is None:
            messagebox.showerror(
                "Missing library",
                "មិនអាចផ្ទុកបណ្ណាល័យ PDF បានទេ:\n{}".format(IMPORT_ERROR)
            )
            return
        if not self.files:
            messagebox.showwarning("មិនទាន់មាន PDF", "សូមបន្ថែមឯកសារ PDF ជាមុន។")
            return

        self.is_processing = True
        self.progress["maximum"] = len(self.files)
        self.progress["value"] = 0
        self.status_var.set("កំពុងដំណើរការ...")
        threading.Thread(target=self._process_worker, daemon=True).start()

    def _process_worker(self):
        successes = 0
        failures = []
        for index, source in enumerate(self.files, 1):
            try:
                destination_folder = self.output_dir or os.path.dirname(source)
                destination = output_path_for(source, destination_folder)
                page_count = swap_pdf_pages(source, destination)
                successes += 1
                message = "រួចរាល់: {} ({} ទំព័រ)".format(os.path.basename(source), page_count)
            except Exception as exc:
                failures.append("{}: {}".format(os.path.basename(source), exc))
                message = "មានបញ្ហា: {}".format(os.path.basename(source))

            self.root.after(0, self._update_progress, index, message)

        self.root.after(0, self._finish_processing, successes, failures)

    def _update_progress(self, value, message):
        self.progress["value"] = value
        self.status_var.set(message)

    def _finish_processing(self, successes, failures):
        self.is_processing = False
        summary = "បានបញ្ចប់៖ ជោគជ័យ {} / {} ឯកសារ។".format(successes, len(self.files))
        self.status_var.set(summary)
        if failures:
            details = "\n".join(failures[:12])
            if len(failures) > 12:
                details += "\n..."
            messagebox.showwarning("បញ្ចប់ដោយមានបញ្ហាខ្លះ", summary + "\n\n" + details)
        else:
            messagebox.showinfo("ជោគជ័យ", summary + "\nឯកសារថ្មីត្រូវបានរក្សាទុករួចរាល់។")


def main():
    root = tk.Tk()
    if PdfReader is None:
        messagebox.showerror(
            "Missing library",
            "មិនអាចផ្ទុកបណ្ណាល័យ pypdf បានទេ:\n{}".format(IMPORT_ERROR)
        )
        return
    PDFPageSwapperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
