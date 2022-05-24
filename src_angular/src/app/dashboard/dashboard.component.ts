import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, Validators, FormControl } from '@angular/forms';
import { Router } from '@angular/router';

import { MatPaginator } from '@angular/material/paginator';

import { ErrorDialog } from '../common/common-error';


import { ConnectorService } from '../connector.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatSnackBar } from '@angular/material/snack-bar';
import { interval, Subscription } from 'rxjs';
import { element } from 'protractor';


// Configuration element from Devices Details
export interface DeviceDetailsElement {
  managed: boolean,
  role: string,
  notes: string,
  ip_config: IpConfigElement,
  oob_ip_config: IpConfigElement,
  disable_auto_config: boolean,
  networks: object,
  port_usages: object,
  additional_config_cmds: string[],
  id: string,
  name: string,
  site_id: string,
  org_id: string,
  created_time: number,
  modified_time: number,
  map_id: string | null,
  mac: string,
  serial: string,
  model: string,
  hw_rev: string,
  type: string,
  tag_uuid: string | null,
  tag_id: number | null,
  deviceprofile_id: string | null
}

export interface IpConfigElement {
  type: string,
  ip: string | null,
  netmask: string | null,
  gateway: string | null,
  dns: string[] | null,
  dns_suffix: string | null,
  network: string
}

export interface PortElement {
  mode: string,
  all_networks: boolean,
  networks: string[],
  port_network: string,
  port_auth: string,
  enable_mac_auth: string,
  guest_network: string,
  bypass_auth_when_server_down: boolean,
  speed: string,
  duplex: string,
  disable_autoneg: boolean,
  mac_limit: number,
  stp_edge: boolean,
  mtu: number,
  disabled: boolean,
  poe_disabled: boolean,
  description: string,
  voip_network: string,
  storm_control: {}
}


// Configuration Elements derived from the site
export interface DerivedElement {
  additional_config_cmds: string[],
  network: object,
  port_usages: object,
  switch_matching: SwitchMatchingElement,
  vars: object

}
export interface SwitchMatchingElement {
  element: boolean,
  riles: object[]
}

// Device Elements for the list
export interface DeviceElement {
  id: string,
  site_id: string,
  org_id: string,
  mac: string,
  vc_mac: string,
  model: string,
  type: string,
  serial: string,
  status: string,
  members: object[]
}

export interface MistDevices {
  results: DeviceElement[];
  total: number;
  limit: number;
  page: number;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})


export class DashboardComponent implements OnInit {

  frmPort = this._formBuilder.group({
    mode: "access",
    all_networks: false,
    networks: [],
    port_network: "default",
    port_auth: "",
    enable_mac_auth: "",
    guest_network: "",
    bypass_auth_when_server_down: false,
    speed: ["auto"],
    duplex: ["auto"],
    autoneg: true,
    mac_limit: 0,
    stp_edge: true,
    mtu: 1514,
    enabled: true,
    poe: true,
    description: "",
    voip_network: "",
    storm_control: {}
  })

  defaultConfig = {
    mode: "access",
    all_networks: false,
    networks: [],
    port_network: "",
    port_auth: "",
    enable_mac_auth: "",
    guest_network: "",
    bypass_auth_when_server_down: false,
    speed: "auto",
    duplex: "auto",
    disable_autoneg: false,
    mac_limit: 0,
    stp_edge: true,
    mtu: 1514,
    disabled: false,
    poe_disabled: false,
    description: "",
    voip_network: "",
    storm_control: {}
  }

  headers = {};
  cookies = {};
  host = '';
  self = {};
  search = "";
  orgs = [];
  sites = [];
  maps = [];
  org_id: string = "";
  orgMode: boolean = false;
  site_id: string = "__any__";
  me: string = "";

  topBarLoading = false;
  deviceLoading = false;

  editingDevice = null;
  editingDeviceSettings = null;
  editingPorts = [];
  editingPortNames = [];
  editingPortsStatus = {}
  displayedPorts = {}

  filteredDevicesDatabase: MatTableDataSource<DeviceElement> | null;
  devices: DeviceElement[] = []

  resultsLength = 0;
  displayedColumns: string[] = ["device"];
  private _subscription: Subscription

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(private _router: Router, private _http: HttpClient, private _appService: ConnectorService, public _dialog: MatDialog, private _formBuilder: FormBuilder, private _snackBar: MatSnackBar) { }

  //////////////////////////////////////////////////////////////////////////////
  /////           INIT
  //////////////////////////////////////////////////////////////////////////////

  ngOnInit() {
    const source = interval(60000);

    this._appService.headers.subscribe(headers => this.headers = headers)
    this._appService.cookies.subscribe(cookies => this.cookies = cookies)
    this._appService.host.subscribe(host => this.host = host)
    this._appService.self.subscribe(self => this.self = self || {})
    this._appService.org_id.subscribe(org_id => this.org_id = org_id)
    this._appService.site_id.subscribe(site_id => this.site_id = site_id)
    this._appService.orgMode.subscribe(orgMode => this.orgMode = orgMode)
    
    this.getDevices();

    this._subscription = source.subscribe(s => this.getDevices());

  }

  ngOnDestroy() {
    this._subscription.unsubscribe();
  }


  //////////////////////////////////////////////////////////////////////////////
  /////           LOAD DEVICE LIST
  //////////////////////////////////////////////////////////////////////////////

  getDevices() {
    var body = null
    body = { host: this.host, cookies: this.cookies, headers: this.headers, site_id: this.site_id, full: true }

    if (body) {
      this.topBarLoading = true;
      this._http.post<DeviceElement[]>('/api/devices/', body).subscribe({
        next: data => {
          var tmp: DeviceElement[] = []
          data["results"].forEach(element => {
            if (this.editingDevice && this.editingDevice.mac == element.mac) {
              this.editingDevice = element;
            }
          });
          this.filteredDevicesDatabase = new MatTableDataSource(data["results"]);

          this.filteredDevicesDatabase.paginator = this.paginator;
          this.topBarLoading = false;
        },
        error: error => {
          var message: string = "There was an error... "
          if ("error" in error) { message += error["error"]["message"] }
          this.openError(message)
        }
      })

    }
  }

  //////////////////////////////////////////////////////////////////////////////
  /////           EDIT DEVICE
  //////////////////////////////////////////////////////////////////////////////
  editDevice(device: DeviceElement): void {
    if (device == this.editingDevice) {
      this._discardDevice();
    }
    else {
      this._discardDevice();
      this.editingDevice = device;
      this._getDeviceSettings()
      this._getPortStatus()
    }
  }

  _getDeviceSettings(): void {
    this.deviceLoading = true
    this._http.post<any>('/api/devices/settings/', {
      host: this.host,
      cookies: this.cookies,
      headers: this.headers,
      site_id: this.site_id,
      device_id: this.editingDevice.id
    }).subscribe({
      next: data => {
        this.editingDeviceSettings = data
        this.displayedPorts = data.ports
        this.deviceLoading = false
        this.editingPorts = []
        this.editingPortNames.forEach(element => {
          this.editingPorts.push(this.editingDeviceSettings.ports[element])
        })
      },
      error: error => {
        this.deviceLoading = false
        var message: string = "Unable to load settings for the Device " + this.editingDevice.mac + "... "
        if ("error" in error) { message += error["error"]["message"] }
        this.openError(message)
      }
    })
  }


  _discardDevice(): void {
    this.editingDevice = null;
    this.editingDeviceSettings = null;
    this.editingPorts = [];
    this.editingPortNames = [];
    this.displayedPorts = {};
    this._discardPorts()
  }
  
  powerDraw(member) {
    var percentage = (member.poe.power_draw / member.poe.max_power) * 100
    return percentage
  }
  
  //////////////////////////////////////////////////////////////////////////////
  /////           Ports Status
  //////////////////////////////////////////////////////////////////////////////
  
  _getPortStatus(): void {
    this._http.post<any>('/api/devices/portstatus/', {
      host: this.host,
      cookies: this.cookies,
      headers: this.headers,
      site_id: this.site_id,
      device_mac: this.editingDevice.mac
    }).subscribe({
      next: data => {
        this.editingPortsStatus = data.result
      },
      error: error => {
        this.deviceLoading = false
        var message: string = "Unable to load ports status for the Device " + this.editingDevice.mac + "... "
        if ("error" in error) { message += error["error"]["message"] }
        this.openError(message)
      }
    })
  }
  //////////////////////////////////////////////////////////////////////////////
  /////           EDIT Port
  //////////////////////////////////////////////////////////////////////////////
  selectPortFromSwitchView(portName): void {
    let port = this.editingDeviceSettings.ports[portName]
    this.selectPort(port)
  }
  
  selectPort(port): void {
    if (this.editingPorts.includes(port)) {
      this._deletePort(port);
      if (this.editingPorts.length == 1) {
        this._setPortFields(this.editingPorts[0])
      }
    }
    else {
      this._addPort(port);
      if (this.editingPorts.length == 1) {
        this._setPortFields(this.editingPorts[0])
      } else if (this.editingPorts.length == 2) {
        this._setDefaultPortFielts()
      }
    }
  }
  
  // ADD or REMOVE ports from the editing list
  _addPort(port): void {
    this.editingPorts.push(port);
    this.editingPortNames.push(port.port)
  }
  _deletePort(port): void {
    let index = this.editingPorts.indexOf(port)
    this.editingPorts.splice(index, 1)
    let indexName = this.editingPortNames.indexOf(port.port)
    this.editingPortNames.splice(indexName, 1)
    if (this.editingPorts.length == 0) {
      this._discardPorts()
    }
  }
  
  savePorts(): void {
    this.editingPorts.forEach(element => {
      element["new_conf"] = {
        "mode": this.frmPort.get("mode").value,
        "all_networks": this.frmPort.get("all_networks").value,
        "networks": this.frmPort.get("networks").value,
        "port_network": this.frmPort.get("port_network").value,
        "port_auth": this.frmPort.get("port_auth").value,
        "enable_mac_auth": this.frmPort.get("enable_mac_auth").value,
        "guest_network": this.frmPort.get("guest_network").value,
        "bypass_auth_when_server_down": this.frmPort.get("bypass_auth_when_server_down").value,
        "autoneg": this.frmPort.get("autoneg").value,
        "mac_limit": this.frmPort.get("mac_limit").value,
        "stp_edge": this.frmPort.get("stp_edge").value,
        "mtu": this.frmPort.get("mtu").value,
        "disabled": this.frmPort.get("enabled").value == false,
        "poe_disabled": this.frmPort.get("poe").value == false,
        "description": this.frmPort.get("description").value,
        "voip_network": this.frmPort.get("voip_network").value,
        "storm_control": this.frmPort.get("storm_control").value,
        "duplex": this.frmPort.get("duplex").value,
        "speed": this.frmPort.get("speed").value
      }
    })
    if (this.frmPort.valid) {
      this.topBarLoading = true
      var body = {
        host: this.host,
        cookies: this.cookies,
        headers: this.headers,
        site_id: this.site_id,
        org_id: this.org_id,
        port_config: this.editingPorts,
        device_id: this.editingDevice.id
      }
      this._http.post<any>('/api/devices/update/', body).subscribe({
        next: data => {
          this.topBarLoading = false
          //this.updateFrmDeviceValues(data.result)
          this._getDeviceSettings()
          this.openSnackBar("Device " + this.editingDevice.mac + " successfully updated", "Done")
        },
        error: error => {
          this.topBarLoading = false
          var message: string = "Unable to save changes on Device " + this.editingDevice.mac + "... "
          if ("error" in error) { message += error["error"]["message"] }
          this.openError(message)
        }
      })
    }
  }
  // Reset the ports selection and form
  _discardPorts(): void {
    this.editingPorts = []
    this.editingPortNames = []
    this.frmPort.reset()
  }

  // Set Port Form values
  _setDefaultPortFielts(): void {
    this.updateFrmDeviceValues(this.defaultConfig)
  }
  _setPortFields(port): void {
    var port_usage = ""
    // copy default values
    var config = { ...this.defaultConfig }
    // getting the port_usage profile name at the switch level, and, if none, at the site level
    if ("usage" in port.device) {
      port_usage = port.device.usage
    } else if ("usage" in port.site) {
      port_usage = port.site.usage
    }
    // if there is a configured port_usage, retrieving its configuration at the switch level, and
    // if none, at the site level
    if (port_usage) {
      var port_config = {}
      if (port_usage in this.editingDeviceSettings.device.port_usages) {
        port_config = this.editingDeviceSettings.device.port_usages[port_usage]
      }
      else if (port_usage in this.editingDeviceSettings.site.port_usages) {
        port_config = this.editingDeviceSettings.site.port_usages[port_usage]
      }
      // setting the config object with the port_usage settings
      for (var key in port_config) {
        config[key] = port_config[key]
      }
    }
    this.updateFrmDeviceValues(config)
  }

  canbeChecked(portName): boolean {
    return this.editingPortNames.includes(portName);
  }
  //////////////////////////////////////////////////////////////////////////////
  /////           COMMON
  //////////////////////////////////////////////////////////////////////////////
  updateFrmDeviceValues(config: PortElement): void {
    this.frmPort.reset()
    this.frmPort.controls["port_network"].setValue(config.port_network)
    this.frmPort.controls["autoneg"].setValue(config.disable_autoneg == false)
    this.frmPort.controls["enabled"].setValue(config.disabled == false)
    this.frmPort.controls["poe"].setValue(config.poe_disabled == false)
    if (config.disable_autoneg == true) {
      this.frmPort.controls["duplex"] = new FormControl({ value: config.duplex, disabled: true })
      this.frmPort.controls["speed"] = new FormControl({ value: config.speed, disabled: true })
    } else {
      this.frmPort.controls["speed"].setValue(config.speed)
      this.frmPort.controls["duplex"].setValue(config.duplex)
    }
  }


  sortList(data, attribute) {
    return data.sort(function (a, b) {
      var nameA = a[attribute].toUpperCase(); // ignore upper and lowercase
      var nameB = b[attribute].toUpperCase(); // ignore upper and lowercase
      if (nameA < nameB) {
        return -1;
      }
      if (nameA > nameB) {
        return 1;
      }
      return 0;
    })
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value.trim().toLowerCase();
    this.filteredDevicesDatabase.filter = filterValue.trim().toLowerCase();

    if (this.filteredDevicesDatabase.paginator) {
      this.filteredDevicesDatabase.paginator.firstPage();
    }
  }

  applyPortFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value.trim().toLowerCase();
    this.displayedPorts = {}
    if (filterValue) {
      for (var key in this.editingDeviceSettings.ports) {
        if (key.includes(filterValue)) {
          this.displayedPorts[key] = this.editingDeviceSettings.ports[key]
        }
      }
    } else {
      this.displayedPorts = this.editingDeviceSettings.ports
    }
  }

  back(): void {
    this._router.navigate(["/select"]);
  }

  //////////////////////////////////////////////////////////////////////////////
  /////           DIALOG BOXES
  //////////////////////////////////////////////////////////////////////////////
  // ERROR
  openError(message: string): void {
    const dialogRef = this._dialog.open(ErrorDialog, {
      data: message
    });
  }

  // SNACK BAR
  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 5000,
      horizontalPosition: "center",
      verticalPosition: "top",
    });
  }
}


