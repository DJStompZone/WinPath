# NTPath

A tool for handling path-like objects on Windows systems

## Usage

Instantiate with any Windows path

```python
>>> program_files = NTPath("C:\\Program Files")
```

Use the true division operator (`/`) to join paths

```python
>>> seven_zip_dir = program_files / "7-Zip"
>>> print(seven_zip_dir)
C:\Program Files\7-Zip
```

Certain properties are available, such as extension, basename, and parent

```python
>>> sevenzip_bins = [ea for ea in seven_zip_dir.ls() if ea.ext == ".exe"] 
>>> sevenzip_bins
[NTPath(7z.exe), NTPath(7zFM.exe), NTPath(7zG.exe)]
>>> sevenzip_bins[0].is_file
True
```


