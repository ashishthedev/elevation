# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  #config.vm.box = "ubuntu/xenial64" #https://app.vagrantup.com/boxes/search
  config.vm.box = "bento/ubuntu-18.04" #https://app.vagrantup.com/boxes/search


  config.vm.boot_timeout = 0
  config.vm.provider('virtualbox') do |vb, override|
    vb.memory = 1024*2  #Run command 'free -h' from inside vagrant to see how much memory is allocated.
  end
  
  # config.ssh.forward_agent = true
  # config.ssh.insert_key = false
  
  # Forward ports for modules. The maximum number of modules is 9
  for i in 9080..9089
    config.vm.network :forwarded_port, guest: i, host: i
  end

  config.vm.network :forwarded_port, guest: 9092, host: 9092

  
  config.vm.provision "shell", path: "environment/provision/dotfiles.sh"

  config.vm.provision "shell", path: "environment/provision/ubuntu.sh"

  #config.vm.provision "shell", path: "environment/provision/gcloud.sh"

  #config.vm.provision "shell", path: "environment/provision/node.sh"

  #config.vm.provision "shell", path: "environment/provision/reset-git.sh"

  #config.vm.provision "shell", path: "environment/provision/golang-go.sh"

  #config.vm.provision "shell", path: "environment/provision/k8.sh"

  # config.vm.provision "shell", path: "environment/provision/django2.sh"

  # config.vm.provision "shell", path: "environment/provision/virtualenvwrapper.sh"

  # config.vm.provision "shell", path: "environment/provision/fabric.sh"

  config.vm.provision "shell", path: "environment/provision/app.sh"

end
