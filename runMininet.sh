#!/bin/bash
sudo mn -c

cd ~/pox_module/project

# ensure it is formatted
while getopts "d" opt; do
    case $opt in
        d)
            echo "THIS IS LINE 10"
            shift $((OPTIND-1))
            sudo python injectIntegrationData.py "topologies/$1.py"
            ;;
        *)
            echo "Invalid option"
            shift $((OPTIND-1))
            exit 1
            ;;
    esac
done

echo "THIS IS AFTER THE GETOPTS":
sudo -E python "topologies/$1.py" $2