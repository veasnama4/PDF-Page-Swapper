[Setup]
AppId={{8BCE8C41-8A91-4D88-AF7A-2E47C2A2A103}
AppName=PDF Page Swapper
AppVersion=1.0.0
AppPublisher=PDF Page Swapper
DefaultDirName={autopf}\PDF Page Swapper
DefaultGroupName=PDF Page Swapper
OutputDir=Output
OutputBaseFilename=PDF_Page_Swapper_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=pdf_page_swapper.ico
PrivilegesRequired=lowest
; Build and test on each Windows version/architecture you intend to support.

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
Source: "dist\PDF_Page_Swapper.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\PDF Page Swapper"; Filename: "{app}\PDF_Page_Swapper.exe"; IconFilename: "{app}\PDF_Page_Swapper.exe"
Name: "{autodesktop}\PDF Page Swapper"; Filename: "{app}\PDF_Page_Swapper.exe"; IconFilename: "{app}\PDF_Page_Swapper.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\PDF_Page_Swapper.exe"; IconFilename: "{app}\PDF_Page_Swapper.exe"; Description: "Launch PDF Page Swapper"; Flags: postinstall nowait skipifsilent
