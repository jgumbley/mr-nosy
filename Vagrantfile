Vagrant::configure('2') do |config|
  config.ssh.forward_agent = true
  config.vm.define :kali do |kali|

    kali.ssh.private_key_path = 'provisioning/vagrant/kali-1.0'
    kali.ssh.username =  'root'

    kali.vm.box = 'kali-1.1.0-amd64'
    kali.vm.box_url = 'http://ftp.sliim-projects.eu/boxes/kali-1.1.0-amd64.box'

    kali.vm.synced_folder "../", "/opt/dev/", create: true

    kali.vm.provider "virtualbox" do |v|
      v.gui = true
      v.customize ['modifyvm', :id, '--name', 'kali-mr-noseybox']
      v.customize ['modifyvm', :id, '--memory', 1024]
      v.customize ['modifyvm', :id, '--macaddress3', '0800276cf835']
      end
    end
end
