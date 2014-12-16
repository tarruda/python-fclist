"""Python cffi bridge to fontconfig's FcFontList."""
import cffi


__all__ = ('fclist',)


API = '''
typedef enum {
    FcResultMatch, FcResultNoMatch, FcResultTypeMismatch, FcResultNoId,
    FcResultOutOfMemory
} FcResult;

typedef struct {
    int nfont;
    int sfont;
    void **fonts;
} FcFontSet;

void *FcInitLoadConfigAndFonts();
void *FcNameParse(const char *name);
char *FcNameUnparse(void *pat);
void *FcObjectSetBuild(const char *first, ...);
FcFontSet *FcFontList(void *config, void *pat, void *os);
FcResult FcPatternGetBool(const void *pat, const char *object, int n,
                          int *b);
FcResult FcPatternGetInteger(const void *pat, const char *object, int n,
                             int *b);
FcResult FcPatternGetDouble(const void *pat, const char *object, int n,
                            double *d);
FcResult FcPatternGetString(const void *pat, const char *object, int n,
                            char **rv);
void FcConfigDestroy(void *config);
void FcPatternDestroy(void *pat);
void FcObjectSetDestroy(void *os);
void FcFontSetDestroy(void *fs);
void free(void *ptr);
'''


ffi = cffi.FFI()
ffi.cdef(API)

fc = ffi.dlopen('fontconfig')
keys = {}


def get_bool(font, key, ffi_key, data, ptr):
    ptr = ffi.new('int *')
    if fc.FcPatternGetBool(font, ffi_key, 0, ptr) == fc.FcResultMatch:
        data[key] = bool(ptr[0])


def get_double(font, key, ffi_key, data, ptr):
    ptr = ffi.new('double *')
    if fc.FcPatternGetDouble(font, ffi_key, 0, ptr) == fc.FcResultMatch:
        data[key] = ptr[0]


def get_int(font, key, ffi_key, data, ptr):
    ptr = ffi.new('int *')
    if fc.FcPatternGetInteger(font, ffi_key, 0, ptr) == fc.FcResultMatch:
        data[key] = ptr[0]


def get_string(font, key, ffi_key, data, ptr):
    if fc.FcPatternGetString(font, ffi_key, 0, ptr) == fc.FcResultMatch:
        data[key] = ffi.string(ptr[0])


def build_fc_key_table():
    bool_keys = [
        'antialias',
        'hinting',
        'verticallayout',
        'autohint',
        'globaladvance',
        'outline',
        'scalable',
        'minspace',
        'embolden',
        'embeddedbitmap',
        'decorative',
    ]

    int_keys = [
        'spacing',
        'hintstyle',
        'width',
        'index',
        'rgba',
        'fontversion',
        'lcdfilter',
    ]

    double_keys = [
        'size',
        'aspect',
        'pixelsize',
        'scale',
        'dpi',
    ]

    string_keys = [
        'family',
        'style',
        'aspect',
        'foundry',
        'file',
        'rasterizer',
        'charset',
        'lang',
        'fullname',
        'familylang',
        'stylelang',
        'fullnamelang',
        'capability',
        'fontformat',
    ]

    for key in bool_keys:
        keys[key] = (ffi.new('char[]', key), get_bool,)
    for key in int_keys:
        keys[key] = (ffi.new('char[]', key), get_int,)
    for key in double_keys:
        keys[key] = (ffi.new('char[]', key), get_double,)
    for key in string_keys:
        keys[key] = (ffi.new('char[]', key), get_string,)


build_fc_key_table()
osb_args = [v[0] for v in keys.values()] + [ffi.NULL]


class Font(object):
    def __init__(self, data):
        for key in keys.keys():
            setattr(self, key, data.get(key, None))
        self.style = set(self.style.split())

    def __repr__(self):
        return 'family: {family}, style: {style}'.format(**self.__dict__)


def fclist(**query):
    """Query fontconfig for fonts matching a criteria.

    The query should be specified as keyword arguments. Any key that can be
    used in the fc-list command can also be used here. Return an iterator that
    yields font objects, which contains attributes that correspond to keys in
    the fontconfig.h header.
    """
    config = ffi.gc(fc.FcInitLoadConfigAndFonts(), fc.FcConfigDestroy)
    pat_str = ''.join([':{0}={1}'.format(k, v) for k, v in query.items()])
    pat = ffi.gc(fc.FcNameParse(pat_str), fc.FcPatternDestroy)
    pat_str = ffi.string(ffi.gc(fc.FcNameUnparse(pat), fc.free))
    if pat_str == '' and len(query):
        raise Exception('Invalid search query')
    os = ffi.gc(fc.FcObjectSetBuild(*osb_args), fc.FcObjectSetDestroy)
    fs = ffi.gc(fc.FcFontList(config, pat, os), fc.FcFontSetDestroy)
    ptrs = {
        get_bool: ffi.new('int *'),
        get_int: ffi.new('int *'),
        get_double: ffi.new('double *'),
        get_string: ffi.new('char **'),
    }
    for i in range(fs.nfont):
        data = {}
        for key, (ffi_key, extract,) in keys.items():
            extract(fs.fonts[i], key, ffi_key, data, ptrs[extract])
        yield Font(data)
