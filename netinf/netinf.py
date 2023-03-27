#!/usr/bin/python
import socket

import nmap
import getmac

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from rich.table import Table

print = Console().print



class Netinf:
    def __init__(self) -> None:
        self.ip: str = self.__ip
        self.scanner = nmap.PortScanner()
    

    @property
    def __ip(self) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    
    def scan_connetced_devices(self) -> None:
        self.scanner.scan(f"{self.ip}/24", arguments='-sn')
        
    # def scan_with_ports(self) -> None:
    #     self.scanner.scan(f"{self.ip}/24", arguments='-sS -T4 -p 1-65535')
    
    def scan(self) -> None:
        with Progress(SpinnerColumn(),  TextColumn("[progress.description]{task.description}"),) as prog:
            prog.add_task(description=f"scan connected devices on {self.ip}/24...")
            self.scan_connetced_devices()
        
            table = Table(title="CONNECTED DEVICES", style="green", expand=True)
            table.add_column("HOSTNAME", style="green")
            table.add_column("TYPE", style="blue")
            table.add_column("IP", style="magenta")
            table.add_column("MAC", style="cyan")
            table.add_column("STATE")
            table.add_column("REASON", style="blue")
            
            for host in self.scanner.all_hosts():
                mac = getmac.get_mac_address(ip=host)
                table.add_row(self.scanner[host].hostname(),self.scanner[host].hostnames()[0]["type"], host, mac, self.scanner[host].state(), self.scanner[host]["status"]["reason"], style='none' if mac else 'dim', )
        print(table)

netinf = Netinf()
netinf.scan()

