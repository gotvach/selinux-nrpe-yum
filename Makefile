#
# Grant Hammond <grant.hammond@adfonic.com>
# Fri Jun 21 2013
#
# Makefile as a cheap way to build the SELinux modules in the subdirectories.
#

rpmbuilddirs := RPMS/ SRPMS/ SPEC/ BUILD/ BUILDROOT/ SOURCES/
ignoredirs := tmp/
internaltargets := $(ignoredirs) all tgz help test clean
modules := $(filter-out $(internaltargets),$(MAKECMDGOALS))

moduledir := $(PWD)/src
specfile := $(realpath selinux-nrpe-yum.spec)

# RPMbuild directories
ifdef DESTDIR
 topdir := $(DESTDIR)
else
 topdir := $(PWD)/tmp
endif

# Let's avoid carnage in our working directory and confine rpmbuild to certain
# directories.
specdir := $(PWD)
sourcedir := $(moduledir)
builddir := $(topdir)/BUILD
buildrootdir := $(topdir)/BUILDROOT
rpmdir := $(topdir)/RPMS
srcrpmdir := $(topdir)/SRPMS

help:
	@echo
	@echo " Makefile for cheap way to build the SELinux modules in the subdirectories"
	@echo
	@echo " Examples:"
	@echo
	@echo "  make pp       # Build policy into .pp file"
	@echo "  make rpm      # Build and package module into RPMs"
	@echo "  make clean    # clear out our local tmp/ directory, aka RPM build structure"
	@echo "  make help     # display this help message"
	@echo
	@echo " Use DESTDIR= to build/install/package in a directory of choice. This can be"
	@echo " a directory already containining RPMS, SRPMS etc. directories if you so wish."
	@echo

pp:
	cd $(moduledir) && $(MAKE) -f /usr/share/selinux/devel/Makefile

clean:
	-rm -rf -- $(DESTDIR)tmp/
	-rm -rf -- $(moduledir)/tmp/

# Target name is the directory hosting the SELinux module
rpm: specfile_exists
	@echo
	@echo "=============================================================="
	@echo "                 Building module: $@ "
	@echo "=============================================================="
	@echo
	@rpmbuild -ba --define "%_topdir $(topdir)" \
		  --define "%_specdir $(specdir)" \
		  --define "%_sourcedir $(sourcedir)" \
		  --define "%_builddir $(builddir)" \
		  --define "%_buildrootdir $(buildrootdir)" \
		  --define "%_rpmdir $(rpmdir)" \
		  --define "%_srcrpmdir $(srcrpmdir)" \
		  $(specfile)

specfile_exists:
ifndef specfile
	$(warning "Missing spec file: $(specfile)")
	@false
endif

# vim:set ts=8 noexpandtab shiftwidth=8:
