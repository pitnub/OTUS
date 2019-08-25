# -*- mode: ruby -*-
# vi: set ft=ruby :

servers=[
  {
    :hostname => "shield",
    :ip => "192.168.51.5",
    :box => "centos/7",
    :ram => 2048,
    :cpu => 2
  },
  {
    :hostname => "sword",
    :ip => "192.168.51.66",
    :box => "offensive-security/kali-linux",
    :ram => 2048,
    :cpu => 2
  }
]

Vagrant.configure(2) do |config|
    servers.each do |machine|
        config.vm.define machine[:hostname] do |node|
            node.vm.box = machine[:box]
            node.vm.hostname = machine[:hostname]
            node.vm.network "private_network", ip: machine[:ip]
            node.vm.provider "virtualbox" do |vb|
                vb.customize ["modifyvm", :id, "--memory", machine[:ram]]
            end
        end
    end
end