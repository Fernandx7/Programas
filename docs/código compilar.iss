[Setup]
AppId={{aadfac4a-6e15-482f-b9e1-f1bd9ee09767}}
AppName=Gerador_Endereçamento
AppVersion=2.0
AppPublisher=Fernando Eduardo
DefaultDirName={autopf}\Gerador_Endereçamento
DefaultGroupName=Gerador_Endereçamento
OutputDir=A:\Atualizador-Utilitarios\docs\Programa_Gerar_Endereçador\v2.0\setup
OutputBaseFilename=Setup_enderecador
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "brazil"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "A:\códigos do Atualizador_utilitarios\Programa_Gerar_Endereçador\dist\Programa_Gerar_Endereçador.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "A:\códigos do Atualizador_utilitarios\Programa_Gerar_Endereçador\postcard.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Gerador_Endereçamento"; Filename: "{app}\Programa_Gerar_Endereçador.exe"; IconFilename: "{app}\postcard.ico"
Name: "{commondesktop}\Gerador_Endereçamento"; Filename: "{app}\Programa_Gerar_Endereçador.exe"; IconFilename: "{app}\postcard.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"

[Run]
Filename: "{app}\Programa_Gerar_Endereçador.exe"; Description: "Executar Gerador_Endereçamento"; Flags: nowait postinstall skipifsilent
