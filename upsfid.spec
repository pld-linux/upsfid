
Summary:	Allows to monitor UPS from Fideltronik
Summary(pl.UTF-8):	Narzędzia do monitorowania UPS-ów firmy Fideltronik
Name:		upsfid
Version:	3.1.0
Release:	0.1
Epoch:		1
License:	Free
Group:		Daemons
Source0:	http://www.fideltronik.com.pl/ups/upsmon/software/3x_linux/%{version}/%{name}-%{version}-1.tgz
# Source0-md5:	879d6b961d4bf60158002f5b218f8dbb
Source1:	%{name}-server.init
Source2:	%{name}-client.init
URL:		http://www.fideltronik.com.pl/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	upsmon
Conflicts:	upsmon

%define		_sysconfdir	/etc/ups/fideltronik

%description
Allows to monitor UPS from Fideltronik.

%description -l pl.UTF-8
Narzędzia pozwalające na monitorowanie i bezpieczne zamknięcie systemu
operacyjnego komputera z dołączonym zasilaczem UPS, oraz powiadamianie
stacji roboczych z zainstalowanym UPS Monitor Client.

%package server
Summary:	UPS Monitor Server
Summary(pl.UTF-8):	Serwer monitorujący UPS
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description server
Allows to monitor UPS from Fideltronik. This package contains the UPS
Monitor Server.

%description server -l pl.UTF-8
Serwer ten pozwala na monitorowanie i bezpieczne zamknięcie systemu
operacyjnego komputera z dołączonym zasilaczem UPS, oraz powiadamianie
stacji roboczych z zainstalowanym UPS Monitor Client.

Ważniejsze cechy:
	* monitoring sygnałów "awarii zasilania" i "baterii rozładowanych"
	* bezpieczne zamknięcie systemu operacyjnego
	* uruchamianie skryptów przy każdej zmianie stanu zasilacza UPS
	* wyłączenie zasilacza UPS po zamknięciu systemu
	* zapis historii stanu zasilania "LOG"
	* informowanie stacji roboczych/serwerów w sieci LAN (TCP/IP)
	* prosta instalacja

%package client
Summary:	UPS Monitor Client
Summary(pl.UTF-8):	Klient monitorowanie UPS-ów
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description client
Allows to monitor UPS from Fideltronik. This package contains the UPS
Monitor Client.

%description client -l pl.UTF-8
UPS Monitor Client 2.0 jest programem odbierającym komunikaty z modułu
UPS Monitor Server 2.x poprzez TCP/IP i wykonującym odpowiednie skrypty,
w których można zamieścić polecenie zamknięcia lokalnego systemu.

Ważniejsze cechy:
	* obsługa komunikatów TCP/IP z maksymalnie 5-ciu serwerów (UPS Monitor Server)
	* wykonywanie wybranego skryptu przy kazdej zmianie stanu zdalnego UPS-a
	* dedykowane skrypty dla każdego zdalnego UPS-a
	* łatwa konfiguracja w pliku tekstowym
	* prosta instalacja

%prep
%setup -q -n %{name}-%{version}-1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/sbin,%{_bindir},%{_sysconfdir}/scripts,/etc/rc.d/init.d,/var/log/fideltronik,%{_datadir}/%{name}/www/images}

install cfg/* $RPM_BUILD_ROOT%{_sysconfdir}
install bin/shutdown.sh $RPM_BUILD_ROOT%{_sysconfdir}/scripts
install bin/{upsmonc,upsmons} $RPM_BUILD_ROOT%{_sbindir}
install bin/upsoff $RPM_BUILD_ROOT/sbin
install bin/xmess $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmons
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmonc

%clean
rm -rf $RPM_BUILD_ROOT

%post server
/sbin/chkconfig --add upsmons
if [ -f /var/lock/subsys/upsmons ]; then
	/etc/rc.d/init.d/upsmons restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/upsd start\" to start upsmons daemon."
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/upsmons ]; then
		/etc/rc.d/init.d/upsmons stop 1>&2
	fi
	/sbin/chkconfig --del upsmons
fi

%post client
/sbin/chkconfig --add upsmonc
if [ -f /var/lock/subsys/upsmonc ]; then
	/etc/rc.d/init.d/upsmonc restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/upsc start\" to start upsmonc daemon."
fi

%preun client
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/upsmonc ]; then
		/etc/rc.d/init.d/upsmonc stop 1>&2
	fi
	/sbin/chkconfig --del upsmonc
fi

%files server
%defattr(644,root,root,755)
%doc README
%attr(750,root,root) %{_sbindir}/upsmons
%attr(750,root,root) /sbin/upsoff
%attr(750,root,root) %dir /etc/ups
%attr(750,root,root) %dir %{_sysconfdir}
%attr(750,root,root) %dir %{_sysconfdir}/scripts
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/scripts/*.sh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/options.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ups.cfg
%attr(754,root,root) /etc/rc.d/init.d/upsmons
%dir /var/log/fideltronik

%files client
%defattr(644,root,root,755)
%doc README
%attr(750,root,root) %{_sbindir}/upsmonc
%attr(750,root,root) %dir /etc/ups
%attr(750,root,root) %dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/options.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upsmonc.dat
%attr(754,root,root) /etc/rc.d/init.d/upsmonc
%dir /var/log/fideltronik
