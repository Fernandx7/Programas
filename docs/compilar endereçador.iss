[Setup]
AppId={{aadfac4a-6e15-482f-b9e1-f1bd9ee09767}}
AppName=Gerador_Endereçamento
AppVersion=2.0
AppPublisher=Fernando Eduardo
DefaultDirName={autopf}\Gerador_Endereçamento
DefaultGroupName=Gerador_Endereçamento
OutputDir=A:\programas\Programas\docs\Gerar_Endereçador\versions\v1.0
OutputBaseFilename=Setup_enderecador
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "brazil"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "A:\programas\Programas\docs\Gerar_Endereçador\dist\endereçador.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "A:\programas\Programas\docs\Gerar_Endereçador\postcard.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Gerador_Endereçamento"; Filename: "{app}\Gerar_Endereçador.exe"; IconFilename: "{app}\postcard.ico"
Name: "{commondesktop}\Gerador_Endereçamento"; Filename: "{app}\Gerar_Endereçador.exe"; IconFilename: "{app}\postcard.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"

[Run]
Filename: "{app}\Gerar_Endereçador.exe"; Description: "Executar Gerador_Endereçamento"; Flags: nowait postinstall skipifsilent
