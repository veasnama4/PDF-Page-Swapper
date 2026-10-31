# PDF Page Swapper — Project

កម្មវិធីនេះប្ដូរទំព័រ PDF ជាគូៗ៖ 1↔2, 3↔4, 5↔6 ...  
បើចំនួនទំព័រជាចំនួនសេស ទំព័រចុងក្រោយនៅដដែល។ ឯកសារដើមមិនត្រូវបានកែប្រែទេ។

## ឯកសារនៅក្នុង Project
- `pdf_page_swapper.py` — កូដកម្មវិធី
- `pdf_page_swapper.ico` — Logo/Icon សម្រាប់ EXE, Window និង Shortcut
- `pdf_page_swapper_logo.png` — រូប Logo ដើមជាទម្រង់ PNG
- `build_portable.bat` — បង្កើត Portable EXE
- `build_installer.bat` — បង្កើត Installer EXE
- `installer.iss` — ការកំណត់ Inno Setup
- `requirements.txt` — បណ្ណាល័យដែលត្រូវការ

## មិនត្រូវការ .NET Framework
កម្មវិធីនេះត្រូវបានសរសេរដោយ Python និងខ្ចប់ជាឯកសារ EXE ដោយ PyInstaller។ វាមិនប្រើ .NET Framework ទេ។ នៅលើកុំព្យូទ័រដែលយកទៅប្រើ អ្នកមិនចាំបាច់ដំឡើង .NET, Python ឬបណ្ណាល័យ pypdf ដាច់ដោយឡែកទេ បន្ទាប់ពីបានបង្កើត EXE រួច។ គ្រាន់តែចម្លង EXE ទៅកុំព្យូទ័រ Windows ដែលត្រូវគ្នា ហើយបើកប្រើ។

## ការបង្កើត EXE លើ Windows
សម្រាប់គោលដៅ Windows 7 SP1 ឡើងទៅ សូមប្រើ Python 3.8.10 ដែលសមស្របនឹងស្ថាបត្យកម្ម Windows របស់អ្នក។ Python 3.8 ជាជំនាន់ចុងក្រោយដែលគាំទ្រ Windows 7។

1. ដំឡើង Python 3.8.10 លើកុំព្យូទ័រដែលប្រើសម្រាប់ Build ប៉ុណ្ណោះ ហើយជ្រើស `Add Python to PATH`។
2. បើក Folder នេះ។ កុំព្យូទ័រអ្នកប្រើចុងក្រោយមិនចាំបាច់មាន Python ទេ។
3. ចុចពីរដងលើ `build_portable.bat`។ EXE នឹងនៅក្នុង `dist` ហើយប្រើ Logo ដែលបានបញ្ចូលរួច។
4. សម្រាប់ Installer សូមដំឡើង Inno Setup រួចចុច `build_installer.bat`។ Setup EXE នឹងនៅក្នុង `Output`.

## ចំណាំអំពី Windows Compatibility
- គោលដៅរចនាគឺ Windows 7 SP1, 8, 8.1, 10 និង 11។
- មិនអាចធានាការដំណើរការលើ Windows ជំនាន់ចាស់ទាំងអស់ ឬគ្រប់ hardware ដោយមិនសាកល្បងបានទេ។
- EXE ត្រូវបង្កើតលើ Windows។ ការបង្កើត x86 និង x64 ត្រូវធ្វើដោយ Python/PyInstaller ដែលមាន architecture ត្រូវគ្នា។
- Windows 7 អាចត្រូវការ Windows updates/runtime ដែលសមស្រប។
- សូមសាកល្បងលើ Windows គោលដៅ មុនចែកចាយឱ្យអ្នកដទៃប្រើ។

## សុវត្ថិភាពឯកសារ
កម្មវិធីសរសេរឯកសារថ្មីដែលមានឈ្មោះ `_swapped_pairs.pdf` ហើយមិនសរសេរជាន់ឯកសារដើមទេ។
PDF ដែលមាន password មិនស្គាល់ ឬមានរចនាសម្ព័ន្ធខូច អាចមិនដំណើរការ។
Metadata មូលដ្ឋានត្រូវបានចម្លង ប៉ុន្តែ bookmark, form fields, digital signatures និងឯកសារភ្ជាប់មិនត្រូវបានធានាថារក្សាទុកទាំងអស់ទេ។
