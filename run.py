import ctypes
import ctypes.wintypes

user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32')

WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_int64, ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)

class WNDCLASSEX(ctypes.Structure): 
  _fields_ = [
    ('cbSize', ctypes.c_uint),
    ('style', ctypes.wintypes.UINT),
    ('lpfnWndProc', WNDPROC),
    ('cbClsExtra', ctypes.c_int),
    ('cbWndExtra', ctypes.c_int),
    ('hInstance', ctypes.wintypes.HINSTANCE),
    ('hIcon', ctypes.wintypes.HICON),
    ('hCursor', ctypes.c_void_p),
    ('hbrBackground', ctypes.wintypes.HBRUSH),
    ('lpszMenuName', ctypes.c_wchar_p),
    ('lpszClassName', ctypes.c_wchar_p),
    ('hIconSm', ctypes.wintypes.HICON)
  ]
    
def wndproc(hw, msg, wparam, lparam):
  # if create -> message box
  if msg == 0x0001:
    return 0
  elif msg == 0x0005:
    user32.DestroyWindow(hw)
    return 0
  elif msg == 0x0012:
    user32.PostQuitMessage(0)
    return 0
  return user32.DefWindowProcW(hw, msg, wparam, ctypes.c_int64(lparam))

wndproc_callback = WNDPROC(wndproc)

# Register the window class
wndclass = WNDCLASSEX()
wndclass.cbSize = ctypes.sizeof(WNDCLASSEX)
wndclass.style = 0
wndclass.lpfnWndProc = wndproc_callback
wndclass.cbClsExtra = 0
wndclass.cbWndExtra = 0
wndclass.hInstance = kernel32.GetModuleHandleW(None)
wndclass.hIcon = None
wndclass.hCursor = None
wndclass.hbrBackground = None
wndclass.lpszMenuName = None
wndclass.lpszClassName = 'RAPYW'
wndclass.hIconSm = None

atom = user32.RegisterClassExW(ctypes.byref(wndclass))
print(f"wndclass atom: {atom}")
if atom == 0:
  raise RuntimeError('RegisterClassEx failed')

# Create the window

WS_OVERLAPPED = 0x00000000
WS_CAPTION = 0x00C00000
WS_SYSMENU = 0x00080000
WS_THICKFRAME = 0x00040000
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_OVERLAPPEDWINDOW = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX

hwnd = user32.CreateWindowExW(
  0,
  'RAPYW',
  'Hello, Windows!',
  WS_OVERLAPPEDWINDOW,
  100, 100, 400, 400,
  None,
  None,
  wndclass.hInstance,
  None
)
print(f"hwnd: {hwnd}")
if hwnd == 0:
  raise RuntimeError('CreateWindowEx failed')

user32.ShowWindow(hwnd, 1)
user32.UpdateWindow(hwnd)
user32.SetForegroundWindow(hwnd)

msg = ctypes.wintypes.MSG()

def update():
  global hwnd, msg
  while hwnd:
    if user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
      user32.TranslateMessage(ctypes.byref(msg))
      user32.DispatchMessageW(ctypes.byref(msg))
      if msg.message == 0x0012: return False
    else: return True
  return False

while update():
  pass
