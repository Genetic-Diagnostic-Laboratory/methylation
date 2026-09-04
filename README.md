# Methylation Tools

Command line tools for qPCR methylation data. Two workflows:

- **analysis**: reads a raw export, flags outlier wells to omit, picks controls and a reference sample per target.
- **report**: reads two target exports, fills an Excel template, runs its macros, and writes one `.xlsm` report per sample.

## Requirements

| | analysis | report |
|---|---|---|
| 64-bit Windows | yes | yes |
| Desktop Microsoft Excel | no | yes |

The report drives Excel through COM automation and runs VBA macros in the template. Excel Online will not work.

## Install

No Python needed. Copy three files to the target machine:

1. `methyl.exe`
2. `qs6_bws_template.xlsm`
3. `qs6_rss_template.xlsm`

The templates are not bundled in the exe. They are referenced by path, so they must be copied separately.

Put `methyl.exe` anywhere, for example `%LOCALAPPDATA%\Programs\methyl\`. Its location does not matter, because settings are stored in your home folder.

If the templates arrived by email or download, right-click each one, open Properties, and click **Unblock**. Otherwise Excel opens them read-only and the macros will not run.

### Optional: run `methyl` from any folder

Without this you must use the full path to the exe. Run once in PowerShell, then open a new terminal:

```powershell
$dir = "$env:LOCALAPPDATA\Programs\methyl"
$p = [Environment]::GetEnvironmentVariable("Path","User")
if ($p -notlike "*$dir*") {
  [Environment]::SetEnvironmentVariable("Path", "$p;$dir", "User")
}
```

## First run

Point the tool at the templates:

```
methyl config set-template bws
methyl config set-template rss
methyl config show
```

Each opens a file picker. `config show` lists the saved paths.

## Usage

```
methyl analysis run                        Launch the analysis tool
methyl report run                          Launch the report generator
methyl config show                         Print current settings
methyl config set-template bws|rss         Choose a report template
methyl config set-positive-control NAME    Set the positive control (default HCT116)
methyl --help                              Show all commands
```

Both `run` commands are interactive. They open a file picker, then prompt in the console.

### analysis run

Select one raw export. Prints the wells to omit, the three selected controls, and the reference sample for each target.

### report run

Select the two target exports, then the destination folder. Assay type comes from the filename: `BWS...` uses targets ICR1 and ICR2, `RSS...` uses PEG1 and GRB.

You then choose to process all samples or one, and pick three controls for each target. Controls are any sample with "control" in its name. At least three must be on the plate.

Reports are named `{sample}_{plate}_{initials}.xlsm`.

## Configuration

Settings live in `C:\Users\<name>\.methylation_config.json`, created on first save. It is per user, so each account configures its own templates.

| Key | Set by |
|---|---|
| `template_bws`, `template_rss` | `config set-template` |
| `positive_control` | `config set-positive-control` |
| `last_directory`, `last_output_directory` | saved automatically |

Remembered directories that no longer exist are ignored, so a config copied between machines will not break.

## Troubleshooting

**"Windows protected your PC"**
The exe is unsigned. Click **More info**, then **Run anyway**. Some corporate antivirus quarantines it outright, which needs an IT allowlist.

**Report saves but RAW DATA and Summarized Data are empty**
Macros were blocked. The console shows `Failed to execute 'Transfer_stepOne_to_Raw'`. Add both the template folder and the output folder as Excel Trusted Locations: File, Options, Trust Center, Trust Center Settings, Trusted Locations. For a network share also tick *Allow Trusted Locations on my network*.

**"No BWS template has been set"**
Run `methyl config set-template bws`.

**First launch is slow**
Expected. The exe unpacks to a temp folder on each run.

## Development

```
python -m venv .venv
.venv\Scripts\pip install -e .
.venv\Scripts\python -m cli.main --help
```

An editable install puts the packages on `sys.path`. Run everything from the repo root:

```
python -m cli.main report run
python -m unittest analysis.processor.test_processor
```

Layout:

| Path | Contents |
|---|---|
| `cli/` | Click entry point, commands, settings |
| `core/` | Shared qPCR export reader |
| `analysis/` | Outlier detection and control selection |
| `report/` | Excel report generation via COM |
| `methyl.py` | PyInstaller entry script |
| `methyl.spec` | PyInstaller build config |

## Building the executable

```
.venv\Scripts\pip install pyinstaller
.venv\Scripts\python -m PyInstaller --noconfirm --clean methyl.spec
```

Produces `dist/methyl.exe`, a single 64-bit file of about 34 MB. Build on 64-bit Windows, since the result is architecture specific. PyInstaller is a build tool only and is not listed in `pyproject.toml` dependencies.

To trade the single file for faster startup, replace `EXE(...)` in `methyl.spec` with a `COLLECT` step to produce a folder instead.
