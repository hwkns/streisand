# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

require 'rbconfig'

os = (
  host_os = RbConfig::CONFIG['host_os']
  case host_os
  when /mswin|msys|mingw|cygwin|bccwin|wince|emc/
    :windows
  when /darwin|mac os/
    :macosx
  when /linux/
    :linux
  when /solaris|bsd/
    :unix
  else
    :unknown
  end
)

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.ssh.forward_agent = true
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "private_network", ip: "10.1.2.200"
  config.vm.network :forwarded_port, host: 7070, guest: 7070
  config.vm.network :forwarded_port, host: 8000, guest: 8000

  config.vm.synced_folder ".", "/var/www/streisand", :id => "vagrant-root"
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 4
  end

  config.vm.provision "ansible" do |ansible|
        ansible.playbook = "provision/vagrant.yml"
        ansible.extra_vars = {
          ansible_python_interpreter: "/usr/bin/python3"
        }
  end
end
