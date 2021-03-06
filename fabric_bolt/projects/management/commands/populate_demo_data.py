from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from fabric_bolt.hosts.models import Host, SSHConfig
from fabric_bolt.projects.models import Project, Stage, Configuration


class Command(BaseCommand):

    ssh_private_key = """-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEArBsTE4MxG/x5PVcL4bNgvcIVJPdS2xWzmZkMZMeOkKx5y+Ew
    DWT0nxU6iZn59M4p5B+xcxCzilnu0ljzeooxUbFRR/2jdvuAVEQRXcAFi17WtHP3
    Up7U/t+vBmv2ZNLAlOn6U10rw36+wPmiG/yKTp9kYNfCE9B0+RS/5DPHbR2FS84D
    49vxruJKMH9zW0A0Me+PskOQtKCcDxT966Z2MsNZiPBti5ZK4yrjDYBM8E9PfXzJ
    tlL/j6G8Z8ALm/MA4VypVMUEaRuRu8TfoMoTAeB2ixRYjoTJMi6r8s7WLOXaGmuV
    g3Z1Gj20sdo2Fi5ordBSm+DDxVHxIBE4iRWkAQIDAQABAoIBAB1u4+xKW3O10eYz
    pMyMqNbLAmK4CWt+YqC6E+yIVFFZrdq4QEeKJGuwbbpqotzDBVcGNIrBKHNYvgcr
    PziNubGG6aeuMO6ARIokufOWi1wyc/WYf4uZrkOIbZ5jiFfl0xmkijMHlBxy6JyI
    FLlEj0Ky76/ANmi9FcQjUE3urQRz6CaDHTjNGAK9qlh61GknGSb99E7BhGMigYkY
    tVDw3RdQtaVJD0XcTpT/e6H3u6IelL3GS+F+JYpgHUC2gEMRTX8qluuLk8zjzNV8
    qS0CXmOXNcCKbJjxWVxXubAlclHfLnpAU9s+Dvp3X+qs1N2LdGyNE+LpGvQe9MDp
    Mg0pKaECgYEA2jbW7QGA7mpsUqdzdXLbVTihq5EqjPSLSVbI1h/z+DGVtsgCDwEd
    +7EeB4tU/RNb5Ky+DGWjGEm2Rw+ntjhwO58lMh45eE2Z4vGnfkKo9uOMlWi/yH+b
    tcB8t78cmazZXYK3dZgsjWsXf4FyQ6aJHIvwhN2xQRmGu2hX36S1IRMCgYEAyehO
    KinudGEE7PrEbxt6MoYGL9pupELCE2oKC292PMRharPN7C2+7E+DbsDEfd4t6nEc
    EzOWWADnFNh3VEGrsDwAgjgh8j2vgf35mLIaRXYXXcJlEtBIOVI9yOYOo8GdA/XV
    yiOGVjjHrwVbWXCNULNKUsSmVN67HCOUXmlUHRsCgYBGF5Vj3bbHXkHbLtRkZndT
    YXR0wpVTX32aGhk6xlq8X1kCtC4NGcPCw/qsW7H59Izw4BfPrZn8xDibjMjHPEu4
    qv7soU6+eNa0UgEGCm1xmFfg6huoUGz4rZKiBu4t4pqTcdhyGmY9KqgKmc7VMhoa
    pEymsPstuQBRFEwdly9jJwKBgEcvci+HbRz2/8eVeiA6LdEWU6QXfR7IsqgpoLT7
    bVJrYnU+Q4Hbdw7V0d8Ac8Z0yPd5PY6/h2grmU1OLHQ2WxPdc8h1hfJkMTbBlnhx
    grWutvpFiWEisfQTvNjR06OEpZk52VBVSg2oIy7f0p8sAYbMT43y6znM9WcsXCkV
    NaS1AoGBAM8jX1zQP/jo1PWuwjzX38xyoDeludCmT09YRsC4C41LbI1Wj8mfxrf5
    bQiPkbIZOeTG6ivvPbKbiwF5W+i92W+uUag5kotG+xCQUrWDrj2ELxRbAetT4dRh
    vv+QoeHlCNRQ+2lsHIoqcAPFCXw6HTT5O/0MIAcEZICT7nf6znXX
    -----END RSA PRIVATE KEY-----"""

    ssh_public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCsGxMTgzEb/Hk9Vwvhs2C9whUk91LbFbOZmQxkx46QrHnL4TANZPSfFTqJmfn0zinkH7FzELOKWe7SWPN6ijFRsVFH/aN2+4BURBFdwAWLXta0c/dSntT+368Ga/Zk0sCU6fpTXSvDfr7A+aIb/IpOn2Rg18IT0HT5FL/kM8dtHYVLzgPj2/Gu4kowf3NbQDQx74+yQ5C0oJwPFP3rpnYyw1mI8G2LlkrjKuMNgEzwT099fMm2Uv+PobxnwAub8wDhXKlUxQRpG5G7xN+gyhMB4HaLFFiOhMkyLqvyztYs5doaa5WDdnUaPbSx2jYWLmit0FKb4MPFUfEgETiJFaQB NEVER-USE-IN-PRODUCTION@fabricbolt.io'

    def handle(self, *args, **options):
        project = Project.objects.create(
            name='Demo Project',
            description='This is a demo project for for testing and development purposes. '
                        'This was generated by running fabric-bolt populate_demo_data.',

        )

        stage = Stage.objects.create(
            project=project,
            name='Demo Stage',

        )

        host = Host.objects.create(
            name='sandbox.fabricbolt.io',
            alias='Demo Host',
        )

        stage.hosts.add(host)

        Configuration.objects.create(
            stage=stage,
            project=project,
            key='comment_text',
            task_name='update_sandbox_site',
            data_type=Configuration.STRING_TYPE,
            prompt_me_for_input=True,
            task_argument=True,
        )

        ssh_config = SSHConfig()
        ssh_config.name = 'NEVER USE THIS FOR PRODUCTION - EVERYONE HAS THE KEY'
        ssh_config.private_key_file.save('demo_key_do_not_use.key', ContentFile(self.ssh_private_key))
        ssh_config.public_key = self.ssh_public_key
        ssh_config.remote_user = 'root'
        ssh_config.save()
