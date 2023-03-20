import os
import json
import pandas as pd

def extract_firewall_policies(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    policy_list = []
    policy_dict = None
    inside_config = False

    for line in lines:
        line = line.strip()

        if line == "config firewall policy":
            inside_config = True
        elif line == "end":
            inside_config = False
        elif inside_config:
            if line.startswith('edit'):
                if policy_dict:
                    policy_list.append(policy_dict)
                policy_id = line.split()[1]
                policy_dict = {'policyid': policy_id}
            elif line.startswith('set') and policy_dict:
                key_value = line.split(' ', 2)[1:]
                key, value = key_value[0], key_value[1]
                policy_dict[key] = value

    if policy_dict:
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