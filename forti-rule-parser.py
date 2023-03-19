import os
import json
import re
import pandas as pd

def extract_firewall_policies(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    config_pattern = re.compile(r'config firewall policy(.*?)end', re.DOTALL)
    config_contents = config_pattern.findall(content)

    policy_list = []

    for config_content in config_contents:
        policy_pattern = re.compile(r'(edit.*?next)', re.DOTALL)
        policies = policy_pattern.findall(config_content)

        for policy in policies:
            policy_dict = {}
            policy_lines = policy.split('\n')

            for line in policy_lines:
                line = line.strip()
                if line.startswith('edit'):
                    policy_id = line.split()[1]
                    policy_dict['policyid'] = policy_id
                elif line.startswith('set'):
                    key_value = line.split(' ', 2)[1:]
                    key, value = key_value[0], key_value[1]
                    policy_dict[key] = value

            policy_list.append(policy_dict)

    return policy_list

def main():
    config_files = [f for f in os.listdir() if f.endswith('.conf')]

    with pd.ExcelWriter('output.xlsx') as writer:
        for config_file in config_files:
            policies = extract_firewall_policies(config_file)
            df = pd.DataFrame(policies)
            sheet_name = config_file.split('.')[0]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

if __name__ == "__main__":
    main()
