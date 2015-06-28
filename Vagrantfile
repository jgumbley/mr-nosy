Vagrant::configure('2') do |config|
  config.ssh.forward_agent = true
  config.vm.define :kali do |kali|

    kali.ssh.private_key_path = 'provisioning/vagrant/kali-1.0'
    kali.ssh.username =  'root'

    kali.vm.box = 'kali-1.1.0-amd64'
    kali.vm.box_url = 'http://ftp.sliim-projects.eu/boxes/kali-1.1.0-amd64.box'

    kali.vm.synced_folder ".", "/opt/dev/", create: true

    kali.vm.provider "virtualbox" do |v|
      v.gui = true
      v.customize ['modifyvm', :id, '--name', 'kali-mr-noseybox']
      v.customize ['modifyvm', :id, '--memory', 1024]
      v.customize ['modifyvm', :id, '--macaddress3', '0800276cf835']
    end

    kali.vm.provision "ansible" do |ansible|
      ansible.playbook = "provisioning/provision.yml"
    end

    kali.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--usb', 'on', '--usbehci', 'on']
      # vb.customize ['usbfilter', 'add', '0', '--target', :id,
      #               '--name', 'ATHEROS USB2.0 WLAN [0108]',
      #               '--vendorid', '0x0cf3', '--productid', '0x9271']
    end

    kali.vm.network "forwarded_port", guest: 5000, host: 5000, auto_correct: true

    end
end
