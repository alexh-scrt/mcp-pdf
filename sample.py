from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

# Create PDF
pdf_path = "/mnt/user-data/outputs/secret_ai_infrastructure_guide.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                       rightMargin=72, leftMargin=72,
                       topMargin=72, bottomMargin=18)

# Container for content
story = []

# Define custom styles
styles = getSampleStyleSheet()

# Custom styles with Secret AI colors
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=HexColor('#E3342F'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=HexColor('#1CCBD0'),
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica'
)

h1_style = ParagraphStyle(
    'CustomH1',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=HexColor('#E3342F'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

h2_style = ParagraphStyle(
    'CustomH2',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=HexColor('#1CCBD0'),
    spaceAfter=10,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

h3_style = ParagraphStyle(
    'CustomH3',
    parent=styles['Heading3'],
    fontSize=12,
    textColor=HexColor('#111827'),
    spaceAfter=8,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    textColor=HexColor('#111827'),
    alignment=TA_JUSTIFY,
    spaceAfter=6,
    fontName='Helvetica'
)

bullet_style = ParagraphStyle(
    'CustomBullet',
    parent=styles['BodyText'],
    fontSize=10,
    textColor=HexColor('#111827'),
    leftIndent=20,
    spaceAfter=6,
    fontName='Helvetica'
)

# Title Page
story.append(Spacer(1, 2*inch))
story.append(Paragraph("Secret AI Labs", title_style))
story.append(Paragraph("Confidential AI Infrastructure Guide", subtitle_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Enterprise-grade Intel TDX + NVIDIA H100 Confidential Computing", body_style))
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("Version 1.0.0 | November 2024", body_style))
story.append(PageBreak())

# Table of Contents
story.append(Paragraph("Table of Contents", h1_style))
story.append(Spacer(1, 0.2*inch))

toc_items = [
    "1. Overview",
    "2. Architecture Summary",
    "3. Quick Start",
    "4. Prerequisites",
    "5. Key Concepts",
    "6. Deployment Workflow",
    "7. Documentation",
    "8. Support & Contributing"
]

for item in toc_items:
    story.append(Paragraph(item, bullet_style))
    
story.append(PageBreak())

# 1. Overview
story.append(Paragraph("1. Overview", h1_style))
story.append(Paragraph(
    "This guide contains comprehensive documentation and resources for deploying <b>Confidential AI</b> infrastructure using Intel Trust Domain Extensions (TDX) and NVIDIA H100 GPUs with Confidential Computing capabilities. Our solution enables organizations to run sensitive AI/ML workloads with hardware-enforced isolation and encryption.",
    body_style
))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("What This Enables", h2_style))
capabilities = [
    "<b>Hardware-Encrypted VMs</b> - Guest memory encrypted at the CPU level, inaccessible to host/hypervisor",
    "<b>Confidential GPU Computing</b> - NVIDIA H100 in CC mode with SPDM secure channels",
    "<b>Remote Attestation</b> - Cryptographic proof of VM and GPU integrity",
    "<b>Zero-Trust AI</b> - Run AI models on untrusted cloud infrastructure",
    "<b>Compliance Ready</b> - Meet data sovereignty and privacy regulations (GDPR, HIPAA, etc.)"
]

for cap in capabilities:
    story.append(Paragraph(f"• {cap}", bullet_style))

story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Use Cases", h2_style))

use_cases = [
    "<b>Private AI Training</b> - Train models on sensitive datasets without exposing data to infrastructure providers",
    "<b>Confidential Inference</b> - Deploy proprietary AI models in multi-tenant environments",
    "<b>Regulated Industries</b> - Healthcare, finance, government AI workloads requiring strict data isolation",
    "<b>Multi-Party ML</b> - Collaborative AI training across organizations without sharing raw data"
]

for uc in use_cases:
    story.append(Paragraph(f"• {uc}", bullet_style))

story.append(PageBreak())

# 2. Architecture Summary
story.append(Paragraph("2. Architecture Summary", h1_style))
story.append(Paragraph("QEMU-KVM Virtualization Stack", h2_style))
story.append(Paragraph(
    "Our infrastructure is built on the proven QEMU-KVM virtualization platform, enhanced with Intel TDX for confidential computing. The stack consists of multiple layers working together to provide hardware-isolated, encrypted virtual machines.",
    body_style
))
story.append(Spacer(1, 0.2*inch))

# Architecture layers
arch_layers = [
    ("Guest VM", "Ubuntu 24.04 + NVIDIA Driver + CUDA 12.5+, with encrypted memory and isolated execution"),
    ("OVMF", "TDX-aware UEFI firmware handling TD initialization and measurements"),
    ("QEMU", "User space process providing device emulation and GPU passthrough via VFIO-PCI"),
    ("KVM", "Kernel module with SEAMCALL interface for TD lifecycle management"),
    ("Linux Kernel", "Version 6.9+ with TDX host support, crypto, and IOMMU"),
    ("Hardware", "Intel Emerald Rapids CPU with TDX-SEAM and NVIDIA H100 GPU")
]

for layer, desc in arch_layers:
    story.append(Paragraph(f"<b>{layer}:</b> {desc}", bullet_style))

story.append(PageBreak())

# Intel TDX Section
story.append(Paragraph("Intel TDX Confidential Computing", h2_style))
story.append(Paragraph(
    "Intel TDX creates <b>Trust Domains (TDs)</b> - VMs with hardware-encrypted memory that are completely isolated from the host OS, hypervisor, and other VMs.",
    body_style
))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("Key Security Features:", h3_style))
security_features = [
    "<b>Memory Encryption</b> - All TD memory encrypted with ephemeral, per-VM keys",
    "<b>CPU State Protection</b> - Register contents hidden from host/VMM",
    "<b>Secure EPT</b> - Extended Page Tables managed by TDX Module prevent memory tampering",
    "<b>Attestation</b> - Cryptographic proof (TD Quote) of VM configuration and integrity",
    "<b>No Host Access</b> - Even privileged host software cannot read TD memory or state"
]

for feature in security_features:
    story.append(Paragraph(f"• {feature}", bullet_style))

story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("NVIDIA H100 Confidential Computing", h2_style))
story.append(Paragraph(
    "The NVIDIA H100 GPU can operate in <b>Confidential Computing mode</b> with additional protections including SPDM secure channels and attestation reports.",
    body_style
))

story.append(PageBreak())

# 3. Quick Start
story.append(Paragraph("3. Quick Start", h1_style))
story.append(Paragraph("Minimum Requirements", h2_style))

# Requirements table
req_data = [
    ['Component', 'Requirement'],
    ['CPU', 'Intel Emerald Rapids (4th/5th Gen Xeon) with TDX'],
    ['GPU', 'NVIDIA Hopper H100 (PCIe or SXM)'],
    ['Host OS', 'Ubuntu 24.04 LTS (mandatory)'],
    ['Memory', '128GB+ RAM'],
    ['Storage', '500GB+ NVMe SSD'],
    ['BIOS', 'TDX-SEAM enabled, TME/TME-MT enabled']
]

req_table = Table(req_data, colWidths=[1.5*inch, 4*inch])
req_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#E3342F')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))

story.append(req_table)
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("30-Minute Setup Overview", h2_style))
setup_steps = [
    "Configure BIOS (Enable Intel TDX, TME, TME-MT, SGX)",
    "Clone Intel TDX kernel tree from GitHub",
    "Build and install TDX-enabled kernel",
    "Configure GPU for CC mode using nvidia_gpu_tools.py",
    "Launch confidential VM with GPU passthrough"
]

for i, step in enumerate(setup_steps, 1):
    story.append(Paragraph(f"{i}. {step}", bullet_style))

story.append(PageBreak())

# 4. Prerequisites - abbreviated for length
story.append(Paragraph("4. Prerequisites", h1_style))
story.append(Paragraph("Hardware Requirements", h2_style))
story.append(Paragraph("<b>CPU:</b> Intel Emerald Rapids with TDX. Recommended: 2-socket, 32+ cores per socket.", body_style))
story.append(Paragraph("<b>GPU:</b> NVIDIA H100 with firmware 96.00.5E.00.00 or later.", body_style))
story.append(Paragraph("<b>Memory:</b> Minimum 128GB DDR5, recommended 256GB+ for production.", body_style))

story.append(PageBreak())

# 5. Key Concepts
story.append(Paragraph("5. Key Concepts", h1_style))

concepts = [
    ("Trust Domain (TD)", "Hardware-isolated VM with encrypted memory, the fundamental unit of confidential computing with Intel TDX."),
    ("TDX-SEAM Module", "Privileged firmware managing TD lifecycle, memory encryption, and attestation reports."),
    ("SEAMCALL", "CPU instruction for kernel-to-TDX-SEAM communication."),
    ("SPDM", "Security Protocol for device authentication and encrypted GPU-driver channels."),
    ("Attestation", "Cryptographic proof of VM/GPU integrity and genuine software."),
]

for concept, description in concepts:
    story.append(Paragraph(f"<b>{concept}</b>", h3_style))
    story.append(Paragraph(description, body_style))
    story.append(Spacer(1, 0.1*inch))

story.append(PageBreak())

# 6. Deployment Workflow
story.append(Paragraph("6. Deployment Workflow", h1_style))
story.append(Paragraph("<b>Total Critical Path Duration: 12-16 hours</b>", body_style))
story.append(Spacer(1, 0.2*inch))

phases = [
    ("Phase 1: Hardware & BIOS", "2-4 hours"),
    ("Phase 2: Host OS Prep", "1-2 hours"),
    ("Phase 3: Kernel Build", "2-3 hours"),
    ("Phase 4: QEMU/OVMF Build", "2-3 hours"),
    ("Phase 5: GPU CC Setup", "30 min"),
    ("Phase 6: Guest VM Creation", "1-2 hours"),
    ("Phase 7: Confidential Launch", "30 min"),
    ("Phase 8: Driver & CUDA", "1 hour"),
    ("Phase 9: Attestation", "30 min"),
    ("Phase 10: AI Workload Deploy", "Variable"),
]

for phase, duration in phases:
    story.append(Paragraph(f"<b>{phase}</b> ({duration})", bullet_style))

story.append(PageBreak())

# 7. Documentation
story.append(Paragraph("7. Documentation Resources", h1_style))
story.append(Paragraph("Key documents in the repository:", body_style))
story.append(Paragraph("• QEMU-KVM Architecture Diagram - Interactive HTML visualization", bullet_style))
story.append(Paragraph("• Intel TDX + H100 CC Architecture - Complete stack diagram", bullet_style))
story.append(Paragraph("• Linux Kernel Patching Guide - Step-by-step build instructions", bullet_style))

story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Important Links", h2_style))
story.append(Paragraph("• Intel TDX GitHub: github.com/intel/tdx-linux", bullet_style))
story.append(Paragraph("• NVIDIA nvTrust: github.com/NVIDIA/nvtrust", bullet_style))
story.append(Paragraph("• KVM TDX Patches: github.com/intel-staging/tdx", bullet_style))

story.append(PageBreak())

# 8. Support & Contributing
story.append(Paragraph("8. Support & Contributing", h1_style))
story.append(Paragraph("Production Readiness Checklist", h2_style))

checklist_items = [
    "Hardware procurement with verified TDX/CC support",
    "BIOS updated and configured correctly",
    "TDX kernel built, tested, and validated",
    "GPU Confidential Computing mode enabled",
    "Remote attestation infrastructure deployed",
    "Monitoring and logging configured",
    "Team trained on deployment procedures",
    "Security audit and compliance verified"
]

for item in checklist_items:
    story.append(Paragraph(f"☐ {item}", bullet_style))

story.append(PageBreak())

# License & Disclaimer
story.append(Paragraph("License & Disclaimer", h1_style))
story.append(Paragraph("Software Licenses", h2_style))
story.append(Paragraph("• Intel TDX Kernel Patches: Linux kernel GPL v2", bullet_style))
story.append(Paragraph("• QEMU: GPL v2", bullet_style))
story.append(Paragraph("• OVMF/EDK2: BSD 2-Clause", bullet_style))
story.append(Paragraph("• This Documentation: © 2024 Secret AI Labs", bullet_style))

story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Important Notices", h2_style))

story.append(Paragraph(
    "<b>Hardware Compatibility:</b> Validated for Intel Emerald Rapids + NVIDIA H100. Other combinations may not work.",
    body_style
))
story.append(Paragraph(
    "<b>Production Use:</b> Thoroughly test in non-production environments before deploying to production.",
    body_style
))
story.append(Paragraph(
    "<b>Security:</b> Overall system security depends on proper configuration, patching, and operational practices.",
    body_style
))

story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("Built with ❤️ by Secret AI Labs", h2_style))
story.append(Paragraph("Empowering organizations to run AI workloads with uncompromising security", body_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Last Updated: November 2024 | Version: 1.0.0", body_style))

# Build PDF
doc.build(story)
print(f"PDF generated successfully: {pdf_path}")
