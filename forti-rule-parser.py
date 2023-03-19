import os
import json
import re

def extract_firewall_policies(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    config_pattern = re.compile(r'config firewall policy(.*?)end', re.DOTALL)
    config_content = config_pattern.findall(content)

    if not config_content:
        return []

    policy_pattern = re.compile(r'(edit.*?next)', re.DOTALL)
    policies = policy_pattern.findall(config_content[0])

    policy_list = []

    for policy in policies:
        policy_dict = {}
        policy_lines = policy.split('\n')

        for line in policy_lines:
            if line.strip().startswith('set'):
                key_value = line.strip().split(' ', 2)[1:]
                key, value = key_value[0], key_value[1]
                policy_dict[key] = value

        policy_list.append(policy_dict)

    return policy_list

def main():
    config_files = [f for f in os.listdir() if f.endswith('.conf')]

    for config_file in config_files:
        policies = extract_firewall_policies(config_file)
        output_file = config_file.split('.')[0] + '_output.json'

        with open(output_file, 'w') as file:
            json.dump(policies, file, indent=4)

if __name__ == "__main__":
    main()