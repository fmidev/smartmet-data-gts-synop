%define smartmetroot /smartmet

Name:           smartmet-data-gts-synop
Version:        18.11.16
Release:        1%{?dist}.fmi
Summary:        SmartMet Data GTS SYNOP
Group:          System Environment/Base
License:        MIT
URL:            https://github.com/fmidev/smartmet-data-gts-synop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       smartmet-qdtools
Requires:       bzip2
Requires:       wget

%description
TODO

%prep

%build

%pre

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

mkdir -p .%{smartmetroot}/cnf/cron/{cron.d,cron.hourly}
mkdir -p .%{smartmetroot}/data/incoming/gts/synop
mkdir -p .%{smartmetroot}/editor/in
mkdir -p .%{smartmetroot}/tmp/data/synop_gts
mkdir -p .%{smartmetroot}/logs/data
mkdir -p .%{smartmetroot}/run/data/synop/bin

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.d/synop-gts.cron <<EOF
*/10 * * * * /smartmet/run/data/synop/bin/dosynop.sh 
EOF

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.hourly/clean_data_gts_synop <<EOF
#!/bin/sh
# Clean SYNOP data
cleaner -maxfiles 2 '_synop.sqd' %{smartmetroot}/data/gts/synop
cleaner -maxfiles 2 '_ship.sqd' %{smartmetroot}/data/gts/ship
cleaner -maxfiles 2 '_buoy.sqd' %{smartmetroot}/data/gts/buoy
cleaner -maxfiles 2 '_synop.sqd' %{smartmetroot}/editor/in
cleaner -maxfiles 2 '_ship.sqd' %{smartmetroot}/editor/in
cleaner -maxfiles 2 '_buoy.sqd' %{smartmetroot}/editor/in

# Clean incoming SYNOP data older than 7 days (7 * 24 * 60 = 10080 min)
find %{smartmetroot}/data/incoming/gts/synop -type f -mmin +10080 -delete
find %{smartmetroot}/data/incoming/gts/synop-bufr -type f -mmin +10080 -delete
EOF

install -m 755 %_topdir/SOURCES/smartmet-data-gts-synop/dosynop.sh %{buildroot}%{smartmetroot}/run/data/synop/bin/

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,smartmet,smartmet,-)
%config(noreplace) %{smartmetroot}/cnf/cron/cron.d/synop-gts.cron
%config(noreplace) %attr(0755,smartmet,smartmet) %{smartmetroot}/cnf/cron/cron.hourly/clean_data_gts_synop
%attr(2775,smartmet,gts)  %dir %{smartmetroot}/data/incoming/gts/synop
%{smartmetroot}/*

%changelog
* Fri Nov 16 2018 Mikko Rauhala <mikko.rauhala@fmi.fi> 18.11.16-1.el7.fmi
- Removed -t option
* Tue Oct 3 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.10.3-1.el7.fmi
- Initial Version
