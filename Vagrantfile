# -*- mode: ruby -*-
# vi: set ft=ruby :

# On your host:
# git clone https://github.com/fedora-infra/fmn.sse.git
# cd fmn.sse
# vagrant up
# vagrant ssh -c "cd /vagrant/; python fmn/sse/sse_webserver.py"

Vagrant.configure(2) do |config|
  config.vm.box_url = "http://cloud.centos.org/centos/7/vagrant/x86_64/images/CentOS-7.LibVirt.box"
  config.vm.box = "centos7-minimal-libvirt"
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 15672, host: 15672
  config.vm.synced_folder ".", "/vagrant", type: "sshfs"

  config.vm.provider :libvirt do |domain|
      domain.cpus = 2
      domain.graphics_type = "spice"
      # If you have a heavy load it can take a lot of ram so
      # to be safe 2GB of ram is allocated, it could probably work with 1GB
      domain.memory = 2048
      domain.video_type = "qxl"
  end

  config.vm.provision "shell", inline: "sudo yum install -y python python-devel rabbitmq-server python-pip gcc libffi-devel openssl-devel zeromq-devel python-twisted fedmsg python-pika python-setuptools"

  # For unit tests
  config.vm.provision "shell", inline: "sudo yum install -y python-mock pytest python-pytest-cov"

  config.vm.provision "shell", inline: "pushd /vagrant/; sudo python setup.py develop; popd;"
  config.vm.provision "shell", inline: "rabbitmq-plugins enable rabbitmq_management"
  config.vm.provision "shell", inline: "sudo systemctl enable rabbitmq-server.service"
  config.vm.provision "shell", inline: "sudo systemctl start rabbitmq-server.service"

end
