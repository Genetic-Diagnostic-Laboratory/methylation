# Methylation QS6 Analysis & Report Generation

Command line tools for qPCR methylation data. Two workflows:

- **analysis**: reads a raw export, flags outlier wells to omit, picks controls and a reference sample per target.
- **report**: reads two target exports, fills an Excel template, runs its macros, and writes one `.xlsm` report per sample.

The report drives Excel through COM automation and runs VBA macros in the template.

## Install

No Python needed. Copy to the target machine:

1. The `methyl` folder, containing `methyl.exe` and `_internal`
2. `qs6_bws_template.xlsm` (see `/templates`)
3. `qs6_rss_template.xlsm` (see `/templates`)

Keep the folder together. `methyl.exe` will not run without `_internal` beside it.

Put the folder anywhere, for example `C:\methyl`. Its location does not matter, because settings are stored in your home folder.

## Two ways to use it

**Double-click `methyl.exe`** for a menu of the common tasks. Nothing to set up, and the tool stays open between tasks.

**Or type commands** in PowerShell, as described below. This needs the PATH step or a full path to the exe.

### Optional: run `methyl` from any folder

Without this you must use the full path to the exe. Set `$dir` to the folder holding `methyl.exe`, run once in PowerShell, then open a new terminal:

```powershell
$dir = "C:\Path\To\Folder"
# For example, if you save methyl.exe in a folder called "MyName" in Local Disk (C:), the path would be "C:\MyName"
$p = [Environment]::GetEnvironmentVariable("Path","User")
if ($p -notlike "*$dir*") {
  [Environment]::SetEnvironmentVariable("Path", "$p;$dir", "User")
}
```
After setting the path, close the current PowerShell window and open a new one.
If you choose not to do this set up, in PowerShell, navigate to the folder containing the script and run `./methyl`

## First run

Set the report templates. From the menu, use options 3 and 4. Or by command:

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

Select one raw export (includes all wells and all targets). Prints the wells to omit, the three selected controls, and the reference sample for each target.

### report run

Select the two target exports (export from QuantStudio for each target after omitting wells), then the destination folder. Assay type comes from the filename: `BWS...` uses targets ICR1 and ICR2, `RSS...` uses PEG1 and GRB. It doesn't matter if you pick ICR1 or ICR2 first (similarly, PEG1 and GRB) when prompted to select the exports.

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

**"No module named analysis"**
You are running the venv shim, not the exe. Run `deactivate`, or call the exe by its full path.

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
| `methyl.py` | PyInstaller entry script and double-click menu |
| `methyl.spec` | PyInstaller build config |

## Building the executable

```
.venv\Scripts\pip install pyinstaller
.venv\Scripts\python -m PyInstaller --noconfirm --clean methyl.spec
```

Produces `dist/methyl/`, a 64-bit folder of about 77 MB. Ship the whole folder, zipped. Build on 64-bit Windows, since the result is architecture specific. PyInstaller is a build tool only and is not listed in `pyproject.toml` dependencies.
