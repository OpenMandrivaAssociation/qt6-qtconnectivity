#define beta rc2
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtconnectivity
Version:	6.8.1
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtconnectivity.git
Source:		qtconnectivity-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtconnectivity-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Connectivity module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	cmake(Qt%{major}DBus)
BuildRequires:	cmake(Qt%{major}Gui)
BuildRequires:	cmake(Qt%{major}GuiTools)
BuildRequires:	cmake(Qt%{major}WidgetsTools)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	pkgconfig(libpcsclite)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	qt%{major}-cmake
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} connectivity module

%global extra_files_Bluetooth \
%{_qtdir}/libexec/sdpscanner

%global extra_devel_files_Bluetooth \
%{_qtdir}/lib/cmake/Qt6/FindBlueZ.cmake

%global extra_devel_files_Nfc \
%{_qtdir}/lib/cmake/Qt6/FindPCSCLITE.cmake \
%{_qtdir}/lib/cmake/Qt6BuildInternals/StandaloneTests/QtConnectivityTestsConfig.cmake \
%{_qtdir}/sbom/*

%qt6libs Bluetooth Nfc

%package examples
Summary: Examples for the Qt %{major} Connectivity module
Group: Development/KDE and Qt

%description examples
Examples for the Qt %{major} Connectivity module

%files examples
%{_qtdir}/examples/bluetooth
%{_qtdir}/examples/nfc

%prep
%autosetup -p1 -n qtconnectivity%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
