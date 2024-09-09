provider "ssh" {
  user = "sabeiro"
  auth = {
    private_key = {
      content = file(pathexpand("~/.ssh/id_rsa"))
    }
  }
  server = {
    host = "intertino.it"
    port = 22
  }
}

data "ssh_tunnel" "consul" {
  remote = {
    port = 8500
  }
}

provider "consul" {
  address = data.ssh_tunnel.consul.local.address
  scheme  = "http"
}

data "consul_keys" "keys" {
  key {
    name = "revision"
    path = "secrets/api/password"
  }
}
