# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true

  config.vm.define "fmn" do |fmn|
    fmn.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/36/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-36-1.5.x86_64.vagrant-libvirt.box"
    fmn.vm.box = "f36-cloud-libvirt"
    fmn.vm.hostname = "fmn.tinystage.test"

    fmn.vm.synced_folder '.', '/vagrant', disabled: true
    fmn.vm.synced_folder ".", "/home/vagrant/fmn", type: "sshfs"

    fmn.vm.provider :libvirt do |libvirt|
      libvirt.cpus = 2
      libvirt.memory = 2048 
    end

    fmn.vm.provision "ansible" do |ansible|
      ansible.playbook = "devel/ansible/playbook.yml"
      ansible.config_file = "devel/ansible/ansible.cfg"
      ansible.verbose = true
    end
  end

end
