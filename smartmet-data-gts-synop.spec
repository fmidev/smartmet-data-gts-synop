%define smartmetroot /smartmet

Name:           smartmet-data-gts-synop
Version:        26.5.21
Release:        1%{?dist}.fmi
Summary:        SmartMet Data GTS SYNOP
Group:          System Environment/Base
License:        MIT
URL:            https://github.com/fmidev/smartmet-data-gts-synop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       smartmet-qdtools
Requires:       bzip2

%description
Reads GTS WMO FM-12 (text) and BUFR SYNOP files and converts them to
SmartMet querydata for the data server and the editor.

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

mkdir -p .%{smartmetroot}/cnf/cron/{cron.d,cron.hourly}
mkdir -p .%{smartmetroot}/data/incoming/gts/{synop,synop-bufr}
mkdir -p .%{smartmetroot}/editor/in
mkdir -p .%{smartmetroot}/tmp/data/synop
mkdir -p .%{smartmetroot}/logs/data
mkdir -p .%{smartmetroot}/run/data/synop/bin

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.d/synop-gts.cron <<EOF
*/10 * * * * /smartmet/run/data/synop/bin/dosynop.sh 
*/20 * * * * /smartmet/run/data/synop/bin/dosynop-bufr.sh
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

# Clean SYNOP BUFR data
cleaner -maxfiles 2 '_synop_bufr.sqd' %{smartmetroot}/data/gts/synop-bufr
cleaner -maxfiles 2 '_synop_bufr.sqd' %{smartmetroot}/editor/in

# Clean incoming SYNOP data older than 7 days (7 * 24 * 60 = 10080 min)
find %{smartmetroot}/data/incoming/gts/synop -type f -mmin +10080 -delete
find %{smartmetroot}/data/incoming/gts/synop-bufr -type f -mmin +10080 -delete
EOF

install -m 755 %_topdir/SOURCES/smartmet-data-gts-synop/dosynop.sh %{buildroot}%{smartmetroot}/run/data/synop/bin/
install -m 755 %_topdir/SOURCES/smartmet-data-gts-synop/dosynop-bufr.sh %{buildroot}%{smartmetroot}/run/data/synop/bin/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,smartmet,smartmet,-)
%config(noreplace) %{smartmetroot}/cnf/cron/cron.d/synop-gts.cron
%config(noreplace) %attr(0755,smartmet,smartmet) %{smartmetroot}/cnf/cron/cron.hourly/clean_data_gts_synop
%attr(2775,smartmet,gts)  %dir %{smartmetroot}/data/incoming/gts/synop
%attr(2775,smartmet,gts)  %dir %{smartmetroot}/data/incoming/gts/synop-bufr
%{smartmetroot}/*

%changelog
* Thu May 21 2026 Mikko Rauhala <mikko.rauhala@fmi.fi> 26.5.21-1.el9.fmi
- Decode all subsets in BUFR messages via --subsets
- Harden FM-12 and BUFR scripts: switch to #!/bin/bash, enable set -uo
  pipefail (without -e so SYNOP/SHIP/BUOY conversions stay independent),
  quote every variable expansion, replace legacy backticks with $(),
  guard TERM expansion, and clean tmp on EXIT via trap
- Fix tmp/data/synop creation in spec (was tmp/data/synop_gts)
- Drop unused wget requirement and SHIP/BUOY scaffolding from BUFR script
- Add CI workflow that builds RPMs for Rocky 8/9/10
* Mon Oct 13 2025 Mikko Rauhala <mikko.rauhala@fmi.fi> 25.10.13-1.el9.fmi
- Added BUFR incoming dir
* Thu Mar 7 2019 Mikko Rauhala <mikko.rauhala@fmi.fi> 19.3.7-1.el7.fmi
- Added BUFR script
* Fri Nov 16 2018 Mikko Rauhala <mikko.rauhala@fmi.fi> 18.11.16-1.el7.fmi
- Removed -t option
* Tue Oct 3 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.10.3-1.el7.fmi
- Initial Version
