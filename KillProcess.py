# process killer 
# author: size_t

import ctypes

# getting a handle to kernel32.dll 
k_handle = ctypes.WinDLL("Kernel32.dll") 

# handle to user32.dll
u_handle = ctypes.WinDLL("User32.dll")

# getting access rights
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFFF)

# grab the window name from user32
lpWindowName = ctypes.c_char_p(input("Enter window name to kill: ").encode('utf-8'))

# grab a handle to the process
hWnd = u_handle.FindWindowA(None, lpWindowName)

#  error check to see if we have the handle 
if hWnd == 0:
	print("Error code: (0) - could no grab handle.".format(k_handle.GetLastError()))
	exit(1)
else:
	print("Got handle. . .")

 # get the PID of the process at the handle 
lpdwProcessId = ctypes.c_ulong()

# using a byref to pass a pointer to the value as needed by the API call
response = u_handle.GetWindowThreadProcessId(hWnd, ctypes.byref(lpdwProcessId))

# error check to see if the call has completed 
if response == 0:
	print("Error code: (0) - could no grab PID.".format(k_handle.GetLastError()))
	exit(1)
else: 
	print("Got the PID!")


# opening the process by PID with specific access
dwDesiredAccess = PROCESS_ALL_ACCESS
bInheritHandle = False
dwProcessId = lpdwProcessId

# calling the windows api call to open the process
hProcess = k_handle.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)

# error check to see if we have a valid handle to the proces
if hProcess <= 0:
	print("Error code: (0) - could no grab priv handle.".format(k_handle.GetLastError()))
else:
	print("Got our handle . . .")
	
# send kill to the process
uExitCode = 0x1 

response = k_handle.TerminateProcess(hProcess, uExitCode)

# error check to see if the process was killed 
if response == 0:
	print("Error code: (0) - could not terminate process.".format(k_handle.GetLastError()))
else:
	print("Process says goodbye :)")
	