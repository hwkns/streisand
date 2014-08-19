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
  config.vm.box_check_update = true
  config.vm.box = "streisand"
  config.vm.box_url = "file://./trusty64.box"
  config.vm.network "private_network", ip: "10.1.2.200"
  config.vm.network :forwarded_port, host: 8000, guest: 8000

  if os == :macosx || os == :linux
    config.vm.synced_folder ".", "/home/vagrant/streisand", :id => "vagrant-root", :nfs => true
  else
    config.vm.synced_folder ".", "/home/vagrant/streisand", :id => "vagrant-root"
  end
  config.vm.synced_folder ".", "/vagrant", disabled: true
end
