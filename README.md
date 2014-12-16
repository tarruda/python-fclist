###Python cffi bridge to fontconfig's FcFontList/FcFontMatch

Useful for python programs that need to query information about fonts installed
in the system(use this instead of parsing fc-list output). Requires the
fontconfig shared library installed in a directory that the cffi module can
find.

###Usage

```python
from fclist import fclist, fcmatch

# Print the family, style and file path of monospace/truetype fonts
for font in fclist(spacing='mono', fontformat='TrueType'):
    print font.family, font.style, font.file

# Print the system's default monospace font
print fcmatch('monospace')
```

`fclist` can receive any keyword arguments that can be passed to the `fc-list`
command, and the returned font objects have most attributes defined by
fontconfig.h.

`fcmatch` receives the same pattern that is normally passed to `fc-match`, but
it doesn't support the --all/--sort options(only returns a single font object).
