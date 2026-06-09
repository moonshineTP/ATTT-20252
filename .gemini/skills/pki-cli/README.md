# PKI Manager - Claude Code Skill

This folder contains a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for managing X.509 certificates via the PKI Manager CLI.

## What is a Claude Code Skill?

Claude Code skills are reusable instructions that extend Claude's capabilities for specific tasks. This skill teaches Claude how to use the PKI Manager CLI to manage Certificate Authorities and certificates.

## Installation

### Option 1: Clone and Symlink (Recommended)

Clone this repository and create a symlink:

```bash
# Clone the skill repository
git clone https://github.com/oriolrius/pki-manager-skill.git ~/.local/share/pki-manager-skill

# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Create symlink
ln -s ~/.local/share/pki-manager-skill ~/.claude/skills/pki-cli
```

### Option 2: Direct Clone

Clone directly into the skills directory:

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Clone directly
git clone https://github.com/oriolrius/pki-manager-skill.git ~/.claude/skills/pki-cli
```

### Option 3: Project-Level Skill

To use this skill only within a specific project:

```bash
# Inside your project
mkdir -p .claude/skills
git clone https://github.com/oriolrius/pki-manager-skill.git .claude/skills/pki-cli
```

## Configuration

Before using the skill, you need to configure your PKI Manager credentials:

```bash
# Create config directory
mkdir -p ~/.config/pki-cli

# Create .env file with your credentials
cat > ~/.config/pki-cli/.env << 'EOF'
PKI_API_URL=https://your-pki-server.example.com/api/v1
PKI_OIDC_URL=https://your-iam-server.example.com/realms/realm/protocol/openid-connect/token
PKI_CLIENT_ID=your-client-id
PKI_CLIENT_SECRET=your-client-secret
EOF
```

## Usage

Once installed, Claude Code will automatically use this skill when you ask about:

- Certificate Authority (CA) management
- Certificate issuance, renewal, or revocation
- PKI operations
- X.509 certificate downloads

### Example Prompts

- "List all CAs in PKI Manager"
- "Create a new CA called Internal CA"
- "Issue a server certificate for api.example.com"
- "Download certificate ABC123 as PKCS12"
- "Show expiring certificates"
- "Renew certificate XYZ789"

### Manual Invocation

You can also invoke the skill manually using:

```
/pki-cli
```

## Skill Contents

- `SKILL.md` - The main skill file containing CLI usage instructions
- `README.md` - This installation guide

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- [uv](https://docs.astral.sh/uv/) or [uvx](https://docs.astral.sh/uv/guides/tools/) for running the CLI
- PKI Manager API access with OIDC credentials

## Related Projects

| Project | Description |
|---------|-------------|
| [PKI Manager](https://github.com/oriolrius/pki-manager-web) | Main PKI Manager web application |
| [PKI Manager CLI](https://github.com/oriolrius/pki-manager-cli) | Python CLI tool for PKI Manager |
| [PKI Manager Ansible](https://github.com/oriolrius/pki-manager-ansible) | Ansible Collection for certificate management ([Galaxy](https://galaxy.ansible.com/ui/repo/published/oriolrius/pki_manager/)) |

## Additional Resources

- [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/claude-code/skills)
