# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/precise64"
  config.vm.provision "shell", path: "vagrant_provision.sh"
  config.vm.network :forwarded_port, guest: 22, host: 2222, id: 'ssh'
  config.vm.synced_folder ".", "/vagrant"
  config.vm.hostname = "dev-orra"
  config.vm.provider "virtualbox" do |vb| 
     # Use VBoxManage to customize the VM. For example to change memory:
     vb.customize ["modifyvm", :id, "--memory", "512"]
  end
end
