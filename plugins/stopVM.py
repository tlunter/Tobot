import subprocess

action = 'stopVM'

class stopVM:
	
	def sendInput(self, vmData):
		
		vmSplit = vmData.split()
		
		force = False
		
		if '--force' in vmSplit:
			vmSplit.remove('--force')
			force = True
		
		vm = vmSplit[0]

		output = 'Stopping {0}\n'.format(str(vm))
	
		if force:
			commandInput = ['VBoxManage','controlvm',str(vm),'poweroff']
			
		else:
			commandInput = ['VBoxManage','controlvm',str(vm),'acpipowerbutton']
		
		try:
			commandOutput = subprocess.check_output(commandInput,stderr=subprocess.STDOUT)
	
		except subprocess.CalledProcessError, e:
			output += '{0} is not a valid Virtual Machine'.format(str(vm))
			output += repr(e.output)
		
		else:
			output += 'Stopped {0}'.format(str(vm))
		
		return output
		
		
stopVM = stopVM()