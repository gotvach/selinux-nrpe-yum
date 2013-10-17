selinux-nrpe-yum
================

SELinux policy module to allow check_yum (possibly check_updates too) to work
via NRPE.

Build
-----

On Red Hat like systems the pre-requisite package is selinux-policy which
contains files appropriate for building SELinux modules.

Build just the module:

```
 make pp
```

Build the module and RPMs:

```
 make rpm
```

SELinux Booleans
----------------

Adds two new booleans:

```
 nrpe_use_yum --> on            # allow YUM to be accessible via NRPE.
 nrpe_connect_network --> off   # allow YUM to pull new caches via network.
```

The first allows read-only access to the RPM database and directories, and
/var/tmp.  The second permits the updating of YUM caches using HTTP which
requires TCP/UDP network access and the ability to do DNS lookups.

Context
-------

NRPE checks, scripts or plugins should have the nagios_system_plugin_exec_t
context in order for this policy to be effective.

Caveats
-------

* Does not work with sudo check_yum

I have never found it necessary to run check_yum using sudo even on a SELinux
enabled system. General issues tend to be permissions related of cached files
in /var/tmp/yum-* and /var/cache/yum. And those issues can stem from running
yum with a user that has a more restrictive umask (example case is calling yum
via func)

License
-------

Released under the BSD license with permission of Adfonic Ltd.

Thank you.

Personal Note
-------------

Please bear in mind that whilst I make every effort to be as thorough as
possible (and I spent much time testing/developing), I am not a seasoned
SELinux policy writer. Therefore it should be assumed that there are mistakes
and/or improvements to be found. In which case I would be glad of the feedback!

However, I am pleased with the end result and it is in production use :)

Regards,

Grant

