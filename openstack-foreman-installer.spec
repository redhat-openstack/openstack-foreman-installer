%{?scl:%scl_package openstack-foreman-installer}
%{!?scl:%global pkg_name %{name}}

%global homedir /usr/share/openstack-foreman-installer

Name:	%{?scl_prefix}openstack-foreman-installer
Version:	0.0.18
Release:	3%{?dist}
Summary:	Installer & Configuration tool for OpenStack

Group:		Applications/System
License:	GPLv2
URL:		https://github.com/jsomara/astapor
# source is in github, see corresponding git tags
Source0: http://file.rdu.redhat.com/~jomara/openstack-foreman-installer-%{version}.tar.gz

Patch0: 0001-BZ978568-Fixing-setsebool-for-httpd-on-controller-no.patch

Requires: %{?scl_prefix}ruby
Requires: %{?scl_prefix}puppet
Requires: packstack-modules-puppet
Requires: foreman >= 1.1
Requires: foreman-mysql >= 1.1
Requires: %{?scl_prefix}rubygem-foreman_openstack_simplify
Requires: mysql-server
Requires: augeas

%description
Tools for configuring The Foreman for provisioning & configuration of
OpenStack.

%prep
%setup -n %{pkg_name}-%{version} -q
%patch0 -p1

%build

%install
install -d -m 0755 %{buildroot}%{homedir}
install -d -m 0755 %{buildroot}%{homedir}/bin
install -m 0755 bin/foreman-setup.rb %{buildroot}%{homedir}/bin
install -m 0644 bin/seeds.rb %{buildroot}%{homedir}/bin
install -m 0755 bin/foreman_server.sh %{buildroot}%{homedir}/bin
install -m 0644 bin/foreman-params.json %{buildroot}%{homedir}/bin
install -d -m 0755 %{buildroot}%{homedir}/puppet/modules
cp -Rp puppet/* %{buildroot}%{homedir}/puppet/modules/
install -d -m 0755 %{buildroot}%{homedir}/config
install -m 0644 config/broker-ruby %{buildroot}%{homedir}/config
install -m 0644 config/database.yml %{buildroot}%{homedir}/config
install -m 0775 config/dbmigrate %{buildroot}%{homedir}/config
install -d -m 0755 %{buildroot}%{homedir}/installer_puppet
cp -Rp installer_puppet/* %{buildroot}%{homedir}/installer_puppet/

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
%{homedir}/installer_puppet/
%{homedir}/installer_puppet/*

%changelog
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
