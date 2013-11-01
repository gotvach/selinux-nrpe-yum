%define         modid       yum
%define         module      nrpe_%{modid}
%define         semoduledir /usr/sbin
%define         adfdir      /usr/local/share
#%define         dist        

Name:           selinux-nrpe-%{modid}
Version:        0.3
Release:        1%{?dist}
Summary:        SELinux Policy NRPE for check_yum/check_updates

Group:          Systems Environment/Policy
License:        BSD
URL:            https://github.com/whizzit/selinux-nrpe-yum
#Source0:       https://github.com/
Source1:        %{module}.te
Source2:        %{module}.fc
Source3:        %{module}.if

BuildRequires:  selinux-policy
Requires:       policycoreutils

%description
SELinux policy to allow check_yum (possibly check_updates too) to work on a
SELinux enabled system via an externally driven NRPE check.

Adds two new booleans:

 nrpe_use_yum --> on            # allow YUM to be accessible via NRPE.
 nrpe_connect_network --> off   # allow YUM to pull new caches via network.

The first allows read-only access to the RPM database and directories, and
/var/tmp.  The second permits the updating of YUM caches using HTTP which
requires TCP/UDP network access and the ability to do DNS lookups.

NRPE checks, scripts or plugins should have the nagios_system_plugin_exec_t
context in order for this policy to be effective.

%prep
rm -rf -- selinux/nrpe-%{modid}
mkdir -p selinux/nrpe-%{modid}
install -m 644 %{SOURCE1} selinux/nrpe-%{modid}/
install -m 644 %{SOURCE2} selinux/nrpe-%{modid}/
install -m 644 %{SOURCE3} selinux/nrpe-%{modid}/

%build
cd selinux/nrpe-%{modid}
make -f /usr/share/selinux/devel/Makefile
rm -rf -- tmp/


%install
rm -rf -- $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{adfdir}/selinux/nrpe-%{modid}/
cp -p selinux/nrpe-%{modid}/%{module}.te $RPM_BUILD_ROOT/%{adfdir}/selinux/nrpe-%{modid}/
cp -p selinux/nrpe-%{modid}/%{module}.if $RPM_BUILD_ROOT/%{adfdir}/selinux/nrpe-%{modid}/
cp -p selinux/nrpe-%{modid}/%{module}.fc $RPM_BUILD_ROOT/%{adfdir}/selinux/nrpe-%{modid}/
cp -p selinux/nrpe-%{modid}/%{module}.pp $RPM_BUILD_ROOT/%{adfdir}/selinux/nrpe-%{modid}/


%clean
rm -rf -- $RPM_BUILD_ROOT


%files
%defattr(640,root,root,-)
%{adfdir}/selinux/nrpe-%{modid}/%{module}.te
%{adfdir}/selinux/nrpe-%{modid}/%{module}.if
%{adfdir}/selinux/nrpe-%{modid}/%{module}.fc
%{adfdir}/selinux/nrpe-%{modid}/%{module}.pp


%post
%{semoduledir}/semodule -i %{adfdir}/selinux/nrpe-%{modid}/%{module}.pp


%postun
if [[ "$1" == 0 ]] ; then
    # uninstall = true
    if %{semoduledir}/semodule -l | /bin/grep -q -- %{module}; then
        # unload the module
        %{semoduledir}/semodule -r %{module}
    else
        /bin/echo "Module already unloaded."
    fi
fi
exit 0

%doc


%changelog
* Fri Jun 14 2013 Grant Hammond <grant.hammond@adfonic.com> 0.2-3
  Fix %postun script for upgrading and uninstall!

* Tue Jun 11 2013 Grant Hammond <grant.hammond@adfonic.com> 0.2-2
  SYS-3341: add dist to package name as per Adfonic RPM wiki doc
  SYS-3341: better handling of module removal on uninstall

* Mon Jun 10 2013 Grant Hammond <grant.hammond@adfonic.com> 0.2-1
  SYS-3341: policy to allow networking for YUM to rebuild caches

* Wed Jun 05 2013 Grant Hammond <grant.hammond@adfonic.com> 0.1-1
  SYS-3341: Initial policy draft.

