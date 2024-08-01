import sys
from ctypes import *

WINDOWNAME = 'RAPYW'

def init():
  pass

def react(Text: str):
  print(Text)

################################################################################
################################################################################

def errcheck(result, func, args):
  if result is None or result == 0: raise WinError(get_last_error())
  return result
WNDPROC = WINFUNCTYPE(c_int64, c_void_p, c_uint32, c_uint64, c_int64)
class WNDCLASSW(Structure): _fields_ = [('style', c_uint32), ('lpfnWndProc', WNDPROC), ('cbClsExtra', c_int32), ('cbWndExtra', c_int32), ('hInstance', c_void_p), ('hIcon', c_void_p), ('hCursor', c_void_p), ('hbrBackground', c_void_p), ('lpszMenuName', c_wchar_p), ('lpszClassName', c_wchar_p)]
class POINT(Structure): _fields_ = [('x', c_int32), ('y', c_int32)]
class MSG(Structure): _fields_ = [('hwnd', c_void_p), ('message', c_uint32), ('wParam', c_uint64), ('lParam', c_int64), ('time', c_uint32), ('pt', POINT)]
class COPYDATASTRUCT(Structure): _fields_ = [('dwData', c_uint64), ('cbData', c_uint32), ('lpData', c_void_p)]
kernel32 = WinDLL('kernel32', use_last_error=True); user32 = WinDLL('user32', use_last_error=True); gdi32 = WinDLL('gdi32',use_last_error=True)
kernel32.GetModuleHandleW.argtypes = (c_wchar_p,); kernel32.GetModuleHandleW.restype = c_void_p; kernel32.GetModuleHandleW.errcheck = errcheck
user32.CreateWindowExW.argtypes = (c_uint32, c_wchar_p, c_wchar_p, c_uint32, c_int32, c_int32, c_int32, c_int32, c_void_p, c_void_p, c_void_p, c_void_p); user32.CreateWindowExW.restype = c_void_p; user32.CreateWindowExW.errcheck = errcheck
user32.LoadCursorW.argtypes = (c_void_p ,c_wchar_p); user32.LoadCursorW.restype = c_void_p; user32.LoadCursorW.errcheck = errcheck
user32.RegisterClassW.argtypes = (POINTER(WNDCLASSW),); user32.RegisterClassW.restype = c_uint16; user32.RegisterClassW.errcheck = errcheck
user32.ShowWindow.argtypes = (c_void_p, c_int32); user32.ShowWindow.restype = c_int32
user32.UpdateWindow.argtypes = (c_void_p,); user32.UpdateWindow.restype = c_int32; user32.UpdateWindow.errcheck = errcheck
user32.GetMessageW.argtypes = (POINTER(MSG), c_void_p, c_uint, c_uint); user32.GetMessageW.restype = c_int32; 
user32.TranslateMessage.argtypes = (POINTER(MSG),); user32.TranslateMessage.restype = c_int32
user32.DispatchMessageW.argtypes = (POINTER(MSG),); user32.DispatchMessageW.restype = c_int64
user32.PostQuitMessage.argtypes = (c_int32,); user32.PostQuitMessage.restype = None
user32.DefWindowProcW.argtypes = (c_void_p, c_uint32, c_uint64, c_int64); user32.DefWindowProcW.restype = c_int64
gdi32.GetStockObject.argtypes = (c_int32,); gdi32.GetStockObject.restype = c_void_p

def run():
  wc, msg = WNDCLASSW(), MSG()
  def wndproc(hw, msg, wp, lp):
    global active
    if msg == 0x004A: # WM_COPYDATA
      cds = cast(lp, POINTER(COPYDATASTRUCT)).contents
      react(string_at(cds.lpData, cds.cbData).decode('utf-16'))
      return True
    elif msg == 0x0002: 
      active = False; user32.PostQuitMessage(0); return 0
    return user32.DefWindowProcW(hw, msg, wp, lp)
  wc.style = 0; wc.lpfnWndProc = WNDPROC(wndproc); wc.cbClsExtra = 0; wc.cbWndExtra = 0; wc.hInstance = kernel32.GetModuleHandleW(None); wc.hIcon = None; 
  wc.hCursor = user32.LoadCursorW(None, c_wchar_p(32512)); wc.hbrBackground = None; wc.lpszMenuName = None; wc.lpszClassName = 'RAPYW'
  user32.RegisterClassW(byref(wc))
  hwnd = user32.CreateWindowExW(0, wc.lpszClassName, WINDOWNAME, 12582912 | 524288, -2147483648, -2147483648, 0, 0, None, None, wc.hInstance, None)
  # user32.ShowWindow(hwnd, 1); user32.UpdateWindow(hwnd)
  while user32.GetMessageW(byref(msg), None, 0, 0) > 0:
    user32.TranslateMessage(byref(msg)); user32.DispatchMessageW(byref(msg))
    
if __name__ == '__main__':
  init()
  run()
