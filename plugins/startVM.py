import subprocess

action = 'startVM'

class startVM:
	
	def sendInput(self, vmData):
		
		vmSplit = vmData.split()
		
		vm = vmSplit[0]
		
		output = 'Starting {0}\n'.format(str(vm))
		
		try:
			command = subprocess.check_output(['VBoxManage','startvm',str(vm),'--type','headless'],stderr=subprocess.STDOUT)
		
		except subprocess.CalledProcessError, e:
			output += '{0} is not a valid Virtual Machine'.format(str(vm))
			
		else:
			output += 'Started {0}'.format(str(vm))
		
		return output
		
		
startVM = startVM()