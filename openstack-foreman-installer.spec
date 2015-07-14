%{?scl:%scl_package openstack-foreman-installer}
%{!?scl:%global pkg_name %{name}}
%global upstream_name astapor
%global rel 1

%global homedir /usr/share/openstack-foreman-installer

Name:	%{?scl_prefix}openstack-foreman-installer
Version:	4.0.3
Release:	%{rel}%{?dist}
Summary:	Installer & Configuration tool for OpenStack

Group:		Applications/System
License:	GPLv2
BuildArch:      noarch
URL:		https://github.com/redhat-openstack/%{upstream_name}
# source is in github, see corresponding git tags
Source0: https://github.com/redhat-openstack/%{upstream_name}/archive/openstack-foreman-installer-%{version}.tar.gz

Requires: %{?scl_prefix}ruby
Requires: puppet
Requires: openstack-puppet-modules
Requires: foreman
Requires: foreman-postgresql
Requires: foreman-installer
Requires: foreman-plugin-simplify
Requires: postgresql-server
Requires: augeas

%description
Tools for configuring The Foreman for provisioning & configuration of
OpenStack.

%prep
%setup -n %{upstream_name}-%{pkg_name}-%{version} -q

%build

%install
install -d -m 0755 %{buildroot}%{homedir}
install -d -m 0755 %{buildroot}%{homedir}/bin
install -m 0755 bin/foreman-setup.rb %{buildroot}%{homedir}/bin
install -m 0755 bin/quickstack_defaults.rb %{buildroot}%{homedir}/bin
install -m 0644 bin/seeds.rb %{buildroot}%{homedir}/bin
install -m 0755 bin/foreman_server.sh %{buildroot}%{homedir}/bin
install -m 0644 bin/foreman-params.json %{buildroot}%{homedir}/bin
install -d -m 0755 %{buildroot}%{homedir}/puppet/modules
cp -Rp puppet/modules/* %{buildroot}%{homedir}/puppet/modules/
install -d -m 0755 %{buildroot}%{homedir}/config
install -m 0644 config/broker-ruby %{buildroot}%{homedir}/config
install -m 0644 config/database.yml %{buildroot}%{homedir}/config
install -m 0644 config/hostgroups.yaml %{buildroot}%{homedir}/config
install -m 0644 config/quickstack.yaml.erb %{buildroot}%{homedir}/config
install -m 0775 config/dbmigrate %{buildroot}%{homedir}/config
install -d -m 0755 %{buildroot}%{homedir}/puppet

%files
%{homedir}/
%{homedir}/bin/
%{homedir}/bin/foreman-setup.rb
%{homedir}/bin/quickstack_defaults.rb
%{homedir}/bin/seeds.rb
%{homedir}/bin/foreman_server.sh
%{homedir}/bin/foreman-params.json
%{homedir}/puppet/
%{homedir}/puppet/*
%{homedir}/config/
%{homedir}/config/broker-ruby
%{homedir}/config/dbmigrate
%{homedir}/config/database.yml
%{homedir}/config/hostgroups.yaml
%{homedir}/config/quickstack.yaml.erb

%changelog
* Tue Jul 14 2015 Jason Guiditta <jguiditt@redhat.com> 4.0.3-1
- BZ #1236180 - Missing redis-vip then ceilo-central pcs constraint.
- BZ #1236685 - Add redhat_register snippet.
- BZ #1240789 - Bump pacemaker start timeout for nova api, conductor.
- BZ #1240362 - Update to compute node's cinder/catalog_info.
- BZ #1241628 - Rabbitmq file descriptors.
- Add PLUMgrid plugin support.

* Thu Jun 25 2015 Jason Guiditta <jguiditt@redhat.com> 4.0.2-1
- Add new interleave settings from ref arch.
- Fix constraints to handle ceilometer-central with or without redis.
- Set galera -> keystone constraint to promote.
- Rabbitmq configured on all nodes before pacemaker starts it.
- The manage_repos parameter is deprecated, switch to repos_ensure.
- Puppet-keystone needs tenant/password for identity_service.
- Updated rbd settings in compute's nova.conf.
- Added support for Dell Storage Center Cinder Backend.
- More robust setting of pcs properties.
- Port quickstack to use newer puppet-neutron agent/plugin code.
- Make sure vips are colo before the usual i-am-vip checks.
- Use verify_on_create with pcmk_resource.

* Wed Jun 10 2015 Jason Guiditta <jguiditt@redhat.com> 4.0.1-1
- Fix ceilometer+redis to use vip and have central be a/a.
- Replace python-ceph package dependency with python-rbd.

* Wed Jun 3 2015 Jason Guiditta <jguiditt@redhat.com> 4.0.0-1
- Initial compatibility with kilo build.

* Wed Jan 28 2015 Jason Guiditta <jguiditt@redhat.com> 3.0.13-1
- BZ #1186378 - Change qpid defaults for newer qpid rpms.

* Wed Jan 28 2015 Jason Guiditta <jguiditt@redhat.com> 3.0.12-1
- BZ #1181864 - Installation of OFI displays incorrect admin credentials.
- BZ #1182219 - Add role heat_stack_owner for admin user.

* Fri Jan 23 2015 Jason Guiditta <jguiditt@redhat.com> 3.0.11-1
- BZ #1182176: take account of quickstack::pacemaker::ceilometer::verbose
  parameter.
- BZ #1181796 - neutron 127.0.0.1 /etc/hosts workaround.
- BZ #1182685 - params for Cinder NetApp driver.

* Thu Jan 15 2015 Mike Burns <mburns@redhat.com> 3.0.10-2
- BZ #1182673 - galera load balancer config should use port 9200

* Wed Jan 14 2015 Jason Guiditta <jguiditt@redhat.com> 3.0.10-1
- BZ #1168755 - rabbitmqctl failure while setting HA policy
- BZ #1175869 - Neutron haproxy config was broken.

* Tue Jan 13 2015 Jason Guiditta <jguiditt@redhat.com> 3.0.9-1
- BZ #1179969 - Integrating n1kv installation RHEL-OSP installer in OSP6.
- BZ #1175869 - Change pcs resource creation to use interleave.
- BZ #1176966 - Increase haproxy timeouts for galera proxy.
- BZ #1180708 - Galera proxy should use 'on-marked-down shutdown-sessions'.
- BZ #1175869 - Add constraints for safe reboots.
- BZ #1170113 - Setting multiple active network nodes for Neutron HA.

* Wed Dec 17 2014 Jason Guiditta <jguiditt@redhat.com> 3.0.8-1
- BZ #1167414 - rabbitmq tcp keepalive.
- BZ #1173730 - add default type for new cluster network params.
- BZ #1159390 - Allow open_files_limit & max_connections to be set for galera.
- BZ #1174955 - retry adding galera resource if needed.

* Tue Dec 16 2014 Jason Guiditta <jguiditt@redhat.com> 3.0.7-1
- BZ #1174487 - default galera ssl setting to true.
- Fix setting of auth_url from glance cache.
- BZ #1173730 - allow separation of cluster and management networks.

* Mon Dec 15 2014 Jason Guiditta <jguiditt@redhat.com> 3.0.6-1
- Longer default timeout for mongodb service.
- BZ #1173217 - Errors in /var/log/ceilometer/collector.log.
- BZ #1172366 - fix some pcmk constraints.

* Fri Dec 5 2014 Jason Guiditta <jguiditt@redhat.com> 3.0.5-1
- Juno stability fixes

* Wed Dec 3 2014 Jason Guiditta <jguiditt@redhat.com> 3.0.4-1
- BZ #1168270 -  Set allow_overlapping_ips to True for HA deployments by
  default.
- BZ #1168755 - rabbitmq fix node names.
- Extra ordering enforcement for mongodb+ceilo.

* Fri Nov 28 2014 Jiri Stransky <jistr@redhat.com> 3.0.3-1
- BZ #1168433 - undefined method "to_a" for "ens7":String
- Quickstack Hiera data adjustments

* Tue Nov 25 2014 Jason Guiditta <jguiditt@redhat.com> 3.0.2-1
- Equalogic default setting san_thin_provision should be true.
- BZ #1165008 - Exposing quota related parameters in neutron.conf.
- Fix typo in ceilometer notifier constraint name.
- Use account security from mysql puppet to remove defaults.
- Removed Puppet module NTP.
- Add hostnames into /etc/hosts local to pacemaker cluster.
- BZ #1151438: Add support for network_device_mtu and veth_mtu.
- Switch to using galera resource agent.
- BZ #1167414 - configure TCP keepalive setting.

* Wed Nov 19 2014 Jason Guiditta <jguiditt@redhat.com> 3.0.1-1
- Update quickstack modules to work for juno
- Change foreman_server.sh to use postgres.
- Add Hiera YAML data.
- BZ #1088613 - Add Ceilometer Service to HA hostgroup.
- BZ #1084229 - Add support for configuring SSL for RabbitMQ.

* Wed Nov 12 2014 Jason Guiditta <jguiditt@redhat.com> 3.0.0-1
- Initial build for Juno, puppet modules not yet working

* Mon Oct 27 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.32-1
- BZ #1157340 - need to rerun puppet to deploy heat on HA Controller.
- BZ #1156342 - Memcached port not being opened in HA deployments.

* Thu Oct 23 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.31-1
- BZ #1156183 - open ceph ports on ceph storage node

* Tue Oct 14 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.30-1
- BZ #1150732 - Integrating n1kv installation with OS-HA in RHEL-OSP (bugfix).

* Thu Oct 9 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.29-1
- BZ #1131980 - Fix qpid configuration for Neutron Controllers.
- BZ #1144050 - Create cinder backend types.
- BZ #1124484 - Puppet fails on networker after br-ex is configured.
- BZ #1150732 - Integrating n1kv installation with OSP HA.
- BZ #1150246 - Galera+puppet stability improvements.
- BZ #1149777 - Add host id to neutron.conf.
- BZ #1151176 -  fence_xvm: expose port param, add firewall rule.

* Thu Oct 2 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.28-1
- BZ #1121746 - Integrate n1kv installation with RHEL-OSP installer.
- Add support for Cisco Nexus to HA Neutron.
- BZ #1127236 - Create cron job to flush the keystone tokens.

* Fri Sep 26 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.27-1
- BZ #1142483 - osd pool size, journal size params in ceph.conf.
- BZ #1142528 - open up ceph mon port on controllers.
- BZ #1147077 - Explicitly require rabbitmq service before setting HA policy.

* Fri Sep 19 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.26-1
- BZ #1143311 - ensure libvirt started before set virsh secret.

* Thu Sep 18 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.25-1
- BZ #1143311 - fix template for ceph rbd secret.

* Tue Sep 16 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.24-1
- BZ #1132722 - Cinder volume active/active should be avoided.
- BZ #1123296 - increase rabbitmq haproxy timeout.
- BZ #1135732 - puppet dep cycle error with rbd glance backend.

* Mon Sep 8 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.23-1
- BZ #1126447 - Fix nova scheduler constraints for A/P.
- Add facts for host pacemaker properties.
- BZ #1127863 - ceph client config.
- BZ #1123303 - Add manage_service settings to get puppet out of the way.

* Wed Aug 27 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.22-1
- BZ #1132155 - galera stopped before pcs resource added.

* Fri Aug 15 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.21-1
- BZ #1130304 - nfs-utils should be installed before using nfs.
- BZ #1129896 - HA: openstack-heat-engine fails to start.

* Wed Aug 13 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.20-1
- BZ #1120602 - Add neutron-agent-cleanup ocf resources to Pacemaker config.
- BZ #1128457 - Horizon dashboard -> Not Found.
- BZ #1123301 - nova-metadata VIP/listener is missing on port 8775 in
  haproxy.cfg.
- BZ #1122701 - Incoming ports are wide open.
- BZ #1128361 - Correctly check for openstack-heat-engine service.
- BZ #1125301 - Add heat-engine to cloudwatch colo constraint.

* Tue Aug 12 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.19-1
- BZ #1123300 - haproxy check options missing interval parameter.
- BZ #1123314 - pacemaker heat op monitor interval to 60s.
- BZ #1127862 - ceph client packages (compute, non-ha and ha controller).
- BZ #1126583 -  Unable to connect to instances via VNC.
- BZ #1123312 - increase galera pacemaker start timeout.
- BZ #1129227 - Set l3 external_network_bridge to ''.

* Thu Aug 7 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.18-1
- BZ #1123316 - Add nova-conductor with nova-scheduler to colocation constraint.
- ceph/rbd on compute: add missiing nova.conf param.
- BZ #1123293 - start-failure-is-fatal should be true.
- BZ #1123318 - HA: set max_retries=-1 for accessing the DB.
- BZ #1127816 - HA neutron sets pcs properties before starting service.
- BZ #1127736 - Do not provide a default for network_public_network.
- BZ #1127887 -  HA: rsync not installed on non-galera bootstrap nodes.

* Thu Jul 31 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.17-1
- BZ#1121185 - rabbitmq AMQP traffic should be load balanced across all nodes.
- Use 60 second timeout for galera proxy.
- BZ#1122314 - RabbitMQ clustering fails depending on which node has the VIP.
- ceph/rbd updates and minor fixes to config.
- BZ#1124950 - Quickstack nova compute manifest not setting qpid config.
- controller_common: fixed rabbitmq provider parameters handling for glance.

* Tue Jul 22 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.16-1
- Move params.pp to use class params.
- BZ #1120288 - Avoid race condition in rabbitmq clustering.
- BZ #1121760 - Run clustercheck before setting galera property.

* Tue Jul 15 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.15-1
- Refactor amqp provider selection for HA deployment.
- BZ #1119429 - name rabbitmq nodes with short hostnames.
- BZ #1119485 - Set start-delay on httpd monitor.
- BZ #1118067 - Intermittent incompletion of puppet run on compute nodes.

* Mon Jul 14 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.14-1
- Nova Networking - Set network_size to empty by default.
- Open port 9200 for galera monitor.
- BZ #1118513 - Rsync Get errors with exit code 23.
- BZ #1118826 - Trying to use vlan with Neutron fails install.

* Thu Jul 10 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.13-1
- Change network_floating_range default (nova).
- BZ #1113294 - HA cinder db_sync fails on 2nd and 3rd nodes.
- Remove neutron-db-check, refs to neutron-agents-pre from HA neutron.
- Value interpretation improved for yaml seeding.
- Fix File dep issue for gluster on compute.

* Thu Jul 03 2014 Crag Wolfe <cwolfe@redhat.com> 2.0.12-2
- Add 10s delay to horizon for consistentency with other services
- kvm config in compute nodes by puppet fact
- a less fragile check for cluster_control_ip in pcmk setup
- HA add constraints, start-delays for cinder, glance, heat

* Sun Jun 29 2014 Crag Wolfe <cwolfe@redhat.com> 2.0.11-1
- rm services no longer in howto, neutron-server now a/a
- neutron param defaults that do not cause breakeage
- puppet dep fix
- RabbitMQ HA support

* Thu Jun 26 2014 Crag Wolfe <cwolfe@redhat.com> 2.0.10-2
- Add start-delay to galera (mysqld) pacemaker resource
- Add monitor_params for pacemaker resources
- Ceph RBD changes for HA manifests
- Ceph RBD backend support in glance and cinder
- Disable repo for rabbitmq
- BZ #1110310 - no more ovs core plugin

* Wed Jun 25 2014 Crag Wolfe <cwolfe@redhat.com> 2.0.9-1
- BZ #1110773 - ML2 l2population is missing from plugin.ini config
- HAProxy config for galera must use httpchk
- Rename amqp_server parameter to amqp_provider instead
- remove obsolete A/P mysql manifest/vars from pacemaker
- Added list_params feature and refactored
- BZ #1111656 - Horizon puppet error for HA-all-in-one-controller
- Included quickstack::load_balancer::common
- Add DHCP support to bridge script and usage
- Dell EqualLogic Multi-Instance Cinder Support

* Fri Jun 20 2014 Crag Wolfe <cwolfe@redhat.com> 2.0.8-1
- Refactored quickstack_defaults.rb
- tighten dependencies for keystone and heat
- Fix galera typo
- Fix galera rsync
- Use galera in HA all-in-one host group
- BZ #1111158 - Install the ceilometer alarm evaluator and notifier services
- haproxy configured and running before mysql, keystone, etc

* Wed Jun 18 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.7-1
- BZ #1109311 - Re-add openstack-selinux to deployment.
- BZ #1109250 - auditd not enabled by default.
- BZ #1109329 - Start ceilometer notification agent service.
- BZ #1104219 - Update HA Nova support for Icehouse.
- Pacemaker config cleanup for HA.
- Add script to push values into Foreman.
- BZ #1110504 - nfs-utils missing, cinder can't mount nfs share.
- Ensure Cinder enabled_backends is empty when it should.

* Fri Jun 13 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.6-1
- Neutron and ML2 fixes, default changes.
- Firewall port fix for gre.
- Add Dell EqualLogic backend for Cinder.
- Multi backend support for support for cinder.
- NFS support for cinder.
- HA settings for Keystone and memcached.
- RHEL 7 ipmilan tweaks.

* Mon Jun 09 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.5-1
- BZ #1106517 - Fix file_line changes to horizon.
- Handle differing crm_node output for el6 and el7.
- ML2 icehouse fix.

* Fri Jun 06 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.4-1
- Fix file name for storage_backend::cinder.
- Get Pacemaker operational on RHEL 7 (basics).

* Tue Jun 03 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.3-1
- Add galera server host group (standalone db, not HA).
- Improve check for all nodes to join cluster.
- BZ #1055179 - Rename LVM  Block Storage to Cinder Block storage.
- BZ #1103353 -  Failure during the deployment of glance(utf8).
- BZ #1103315 - Openstack firewall rules are not enabled after reboot.
- BZ #1103271 - Puppet modules need to handle missing openstack-selinux
  gracefully.
- More robust updating of custom pcs properties.
- BZ #1104093 -  Foreman default config is NOT ML2.

* Thu May 29 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.2-1
- Bugfix: Ceilometer starts before mongo is ready.
- Bugfix: Puppet agent fails to run because fencing was off.
- Initial RabbitMQ support (non-HA).

* Wed May 21 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.1-1
- More Bugfixes for HA controllers.
- Initial Gluster Storage hostgroup.
- Parameter cleanups/changes.
- NFS and Gluster backends for Cinder.
- Switch from mysql to mariadb.

* Fri Apr 25 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.0.0-1
- Bugfixes for HA controllers.
- Add support for Foreman 1.5
- Ceilometer/mongo fix.
- Add _network params to deduce ip per machine.

* Fri Apr 11 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.0beta5-1
- BZ #1038766 - Qpid username and password.
- BZ #1086344 - Add Cinder service to HA hostgroup.
- BZ #1083781 - fetch glance user password from pacemaker::params

* Thu Apr 10 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.0beta4-1
- BZ #1075818 - Create New Hostgroup to enable HA deployments.
- BZ #1073087 - [RFE] Use subscription-manager.
- BZ #1049122 - HA Qpid.
- BZ #1083781 - HA Glance fixes.
- BZ #1084534 - Add Nova Service to HA hostgroup.
- BZ #1075818 - Fixes for HA load  balancer.

* Fri Apr 4 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.0beta3-1
- BZ #1083781 - Add Glance Service to HA hostgroup.
- BZ #1082811 - HA Keystone improvements.

* Mon Mar 31 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.0beta2-1
- BZ #1082811 - Add Keystone Service to HA hostgroup.
- BZ #1053623 - openstack-selinux package not installed
- BZ #1064056 - Foreman Heat ports not opened
- Cisco plugin fixes.

* Fri Mar 21 2014 Jason Guiditta <jguiditt@redhat.com> 2.0.0beta1-1
- BZ #1049079 - Use openstack-puppet-modules package.
- BZ #1049121 - Fixes for Ha/Mysql hostgroup.
- BZ #1075818 - Create New HA All-In-One Controller Hostgroup.
- BZ #1075818 - Add HaProxy module managed by pacemaker.
- BZ #1049122 - Add Qpid module managed by pacemaker.
- Add Base Pacemaker module, with fencing configuration.
- Add more flexible provisioning configuration.
- BZ #1068885 - Add option to create a keystonerc_admin file.
- Add admin_host network, defaults to private_host.

* Mon Mar 10 2014 Jason Guiditta <jguiditt@redhat.com> 1.0.5-1
- BZ #1062701 -  Allow configuration of network_managers with nova networking.

* Fri Feb 14 2014 Jason Guiditta <jguiditt@redhat.com> 1.0.4-1
- BZ #1054181 - Set OS description consistently, install LSB.
- BZ #1052408 - HA Mysql manifest: allow creation of neutron db user.
- BZ #1055852 - HTTP 500 Error using Neutron metadata agent.
- BZ #1056892 - Handle interface names containing ".".
- BZ #1049633 - Foreman should support VXLAN.
- BZ #1017281 - Add support for ML2 Core Plugin.
- BZ #1056055 - Create cinder-volumes VG backed by a loopback file.
- BZ #1062664 - Configure qpid_hostname for Controller host groups.
- BZ #1062670 - Add tuned configuration for compute nodes.
- BZ #1056383 - Foreman Controller's swift proxy no longer runs.
- BZ #1055207 - Add localhost and ip access for Horizon UI.
- BZ #1063514 - cinder_gluster_servers default value.
- BZ #998599  - Add options for SSL support using files or FreeIPA.
- BZ #1054498 - Fix double port 80 directives in apache.

* Wed Jan 15 2014 Jason Guiditta <jguiditt@redhat.com> 1.0.3-1
- BZ #1047653 - Cinder LVM setup broken.
- BZ #1053729 - Add missed parameter name change.

* Fri Jan 10 2014 Jason Guiditta <jguiditt@redhat.com> 1.0.2-1
- BZ #1048922 - Package name cannot have array for newer puppet.
- BZ #1050182 - remove the Gluster Storage Host Group.
- BZ #1049688 - Quickstack manifest parameter renaming.
- BZ #1046120 - Remove unused parameter bridge_keep_ip.
- BZ #1015625 - Add selinux support for glusterfs config.
- BZ #1043964 - Fix to move neutron setup after db setup.

* Tue Jan 07 2014 Pádraig Brady <pbrady@redhat.com> 1.0.1-2
- BZ #1048922 - Fix horizon packages install with puppet-3.4

* Fri Dec 20 2013 Crag Wolfe <cwolfe@redhat.com> 1.0.1-1
- BZ #1045132 - l3 external_network_bridge now configurable.
- BZ #1045137 - Ensure physical ports added to ovs bridge on networker.

* Mon Dec 16 2013 Jason Guiditta <jguiditt@redhat.com> 1.0.0-1
- BZ #1042933 - neutron-server fails to start (stamp issue)
- BZ #1040610 Open Ceilometer API port on controller node
- BZ #1042862 Update RHEL OS description
- BZ #1043634 Swift Storage manifest uses incorrect variable

* Tue Dec 10 2013 Jason Guiditta <jguiditt@redhat.com> 0.0.25-1
- BZ #1039661 Fix manifests to work with updated puppet modules
- BZ #1039698 add IPAPPEND 2 to pxe template
- BZ #1040021 Fix enable/disable of heat_cfg and heat_cloudwatch

* Mon Dec 9 2013 Jason Guiditta <jguiditt@redhat.com> 0.0.24-1
- BZ #1038281 - Do not disable selinux on openstack foreman installer.
- BZ #1038772 - Remove Tech Preview text.
- Add Swift Proxy to Controllers, new hostgroup for swift storage.
- Tweak host group configuration/naming.
- Load balancer cleanup, add Swift Proxy.
- Update to work with latest packstack-puppet updates.

* Wed Dec 4 2013 Jason Guiditta <jguiditt@redhat.com> 0.0.23-1
- Refactored Host Groups to make smaller base list
- Gluster backend support for cinder and glance
- Add numerous new config flags
- Add initial neutron vlan support/configs

* Fri Nov 8 2013 Jason Guiditta <jguiditt@redhat.com> 0.0.22-1
- Fix foreman-proxy port conflict
- More installer tweaks
- Neutron, Heat user fixes
- Added external ovs bridge creation
- Remove Clusterlabs repo

* Fri Oct 25 2013 Jason Guiditta <jguiditt@redhat.com> 0.0.21-1
- Configuration improvements for ha mysql
- Update installer to work with foreman 1.3
- Add horizon support to Load Balancer
- Add plugin for cisco nexus to neutron setups

* Tue Oct 22 2013 Jason Guiditta <jguiditt@redhat.com> 0.0.20-1
- Add support for either neutron or nova networking hostgroups.
- Add Cinder, Heat, Ceilometer to Quickstack
- Initial Load Balanced api support
- Initial clustered mysql nodes (pacemaker cluster)
- Set puppet data type in seeds.rb

* Tue Aug 27 2013 Jason Guiditta <jguiditt@redhat.com> 0.0.19-3
- Fixes for Havanna in RDO

* Wed Aug 7 2013 Pádraig Brady <pbrady@redhat.com> 0.0.18-3
- Depend on upstream foreman packages

* Tue Jul 2 2013 Jordan OMara <jomara@redhat.com> 0.0.18-2
- Adding setsebool for proper httpd selinux usage (jomara@redhat.com)

* Fri Jun 21 2013 Jordan OMara <jomara@redhat.com> 0.0.18-1
- fix what interface we derive values from when setting up a subnet.
  (cwolfe@redhat.com)

* Tue Jun 11 2013 Jordan OMara <jomara@redhat.com> 0.0.17-1
- replace "spacewalk" with "satellite" (cwolfe@redhat.com)
- bz972780 add nova conductor to controller (cwolfe@redhat.com)

* Fri Jun 7 2013 Jordan OMara <jomara@redhat.com> 0.0.15-2
- Spec file typo

* Thu Jun 6 2013 Jordan OMara <jomara@redhat.com> 0.0.15-1
- Fixing cinder installation

* Thu Jun 6 2013 Jordan OMara <jomara@redhat.com> 0.0.13-4
- adding db seeds file

* Wed Jun 5 2013 Jordan OMara <jomara@redhat.com> 0.0.13-3
- some spec file changes

* Wed Jun 5 2013 Jordan OMara <jomara@redhat.com> 0.0.13-1
- adding dependency on PackStack modules at runtime
- renaming modules from TryStack to QuickStack
- misc fixes

* Tue May 28 2013 Jordan OMara <jomara@redhat.com> 0.0.5-1
- adding installer puppet code

* Mon May 20 2013 Jordan OMara <jomara@redhat.com> 0.0.1-1
- initial packaging
