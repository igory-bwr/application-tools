#!/usr/bin/env python3 
import json
import os
import sys
import yaml

USAGE=f"""Usage: {sys.argv[0]} <command> [<param...]
    command: 
        help 
        get-service-tags <yaml_file>
        set-tag <yaml_file> <service> <new_tag>
"""

class AppConfig:
    def __init__(self, fname):
        self.file_name = fname
        if not os.path.isfile(self.file_name):
            print("Error: applicattion file is not provided")
            exit(1)
        with open(self.file_name) as yamlFile:
            self.parsed_config = yaml.load(yamlFile)
    def get_services(self):
        return self.parsed_config['services'].keys()
    def get_tag(self, service_name):
        tag = ''
        if service_name in self.get_services():
            tag = self.parsed_config['services'][service_name]['image'].split(':')[1]
        return tag
    def set_tag(self, service_name, tag):
        image_spec = self.parsed_config['services'][service_name]['image'].split(':')[0]
        self.parsed_config['services'][service_name]['image'] = ':'.join([image_spec, tag])
    def get_yaml(self):
        return yaml.dump(self.parsed_config, indent=2)


def print_usage(params = []):
    print(USAGE)

def get_service_tags(params):
    print(f"get_service_tags params: {params}")
    app_file = params[0]
    appconfig = AppConfig(app_file)
    for s in appconfig.get_services():
        print(f"{s}:\t\t{appconfig.get_tag(s)}")

def set_service_tag(params):
    app_file = params[0]
    appconfig = AppConfig(app_file)    
    if params[1] not in appconfig.get_services():
        print(f" the service name {params[1]} doesn't exist" )
        exit(1)
    service_name, new_tag = params[1], params[2]
    appconfig.set_tag( service_name, new_tag)
    for s in appconfig.get_services():
        print(f"{s}:\t\t{appconfig.get_tag(s)}")
    print('************************************')
    print(appconfig.get_yaml())

def get_raw(params):
    app_file = params[0]
    appconfig = AppConfig(app_file) 
    return json.dumps(appconfig.parsed_config, indent=4)

EXECUTE = {
    'get-service-tags': get_service_tags,
    'set-tag': set_service_tag,
    'get-raw': get_raw,
    'help': print_usage
}

def main():
    if len(sys.argv) == 1:
        print_usage() 
        exit(1)
    else:
        command, params = sys.argv[1], sys.argv[2:]
    print(f"command: {command}\nparams: {params}")

    if command not in EXECUTE.keys():
        print("Error: wrong command provided")
        print(USAGE)
        exit(1)

    print(EXECUTE[command](params))
    return 0


if __name__ == "__main__":
    main()
