%{?scl:%scl_package openstack-foreman-installer}
%{!?scl:%global pkg_name %{name}}
%global upstream_name astapor
%global rel 1

%global homedir /usr/share/openstack-foreman-installer

Name:	%{?scl_prefix}openstack-foreman-installer
Version:	1.0.3
Release:	%{rel}%{?dist}
Summary:	Installer & Configuration tool for OpenStack

Group:		Applications/System
License:	GPLv2
BuildArch:      noarch
URL:		https://github.com/redhat-openstack/%{upstream_name}
# source is in github, see corresponding git tags
Source0: https://github.com/redhat-openstack/%{upstream_name}/archive/openstack-foreman-installer-%{version}.tar.gz

Requires: %{?scl_prefix}ruby
Requires: puppet >= 2.7
Requires: packstack-modules-puppet
Requires: foreman >= 1.1
Requires: foreman-mysql >= 1.1
Requires: foreman-installer >= 1.3
Requires: foreman-plugin-simplify
Requires: mysql-server
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
install -m 0644 bin/seeds.rb %{buildroot}%{homedir}/bin
install -m 0755 bin/foreman_server.sh %{buildroot}%{homedir}/bin
install -m 0644 bin/foreman-params.json %{buildroot}%{homedir}/bin
install -d -m 0755 %{buildroot}%{homedir}/puppet/modules
cp -Rp puppet/modules/* %{buildroot}%{homedir}/puppet/modules/
install -d -m 0755 %{buildroot}%{homedir}/config
install -m 0644 config/broker-ruby %{buildroot}%{homedir}/config
install -m 0644 config/database.yml %{buildroot}%{homedir}/config
install -m 0775 config/dbmigrate %{buildroot}%{homedir}/config
install -d -m 0755 %{buildroot}%{homedir}/puppet

%files
%{homedir}/
%{homedir}/bin/
%{homedir}/bin/foreman-setup.rb
%{homedir}/bin/seeds.rb
%{homedir}/bin/foreman_server.sh
%{homedir}/bin/foreman-params.json
%{homedir}/puppet/
%{homedir}/puppet/*
%{homedir}/config/
%{homedir}/config/broker-ruby
%{homedir}/config/dbmigrate
%{homedir}/config/database.yml

%changelog
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

* Mon Dec 10 2013 Jason Guiditta <jguiditt@redhat.com> 0.0.25-1
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
