.PHONY: ssh
ssh:
	docker exec -w /workspaces/aws-identity-center-config-file-generator -it vscode-devcontainer_aws-identity-center-config-file-generator bash
