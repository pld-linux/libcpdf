Summary:	PDF manipulating library
Name:		libcpdf
Version:	2.02r1
%define		fileversion 202r1
%define		minorversion 2
Release:	1
License:	Free for non-commercial use
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	http://www.fastio.com/clibpdf%{fileversion}.tar.gz
Source1:	%{name}-examples.Makefile
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-config.patch
URL:		http://www.fastio.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	zlib-devel
Requires:	xpdf
Requires:	ghostscript-fonts

%description
This is a library of ANSI C functions, for creating PDF files directly
via C.

%package devel
Summary:	Header files needed for libcpdf development
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Requires:	zlib-devel

%description devel
This package includes the header files for developing programs using
libcpdf.

%package static
Summary:	Static libraries needed for libcpdf development
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}
Requires:	zlib-devel

%description static
This package includes static libcpdf libraries.

%prep
%setup -q -n ClibPDF
%patch0 -p0
%patch1 -p0

cp -f %{SOURCE1} examples/Makefile

%build
cd sourceP
%{__make} -f Makefile.Linux shlib \
	CFLAGS="%{rpmcflags} -DLinux -fPIC" \
	VERSION="%{version}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_bindir},%{_mandir}/man1}

install sourceP/cpdflib.h $RPM_BUILD_ROOT%{_includedir}
#install -m 755 %{name}.so.%{version} $RPM_BUILD_ROOT%{_libdir}
install sourceP/libcpdf.so* $RPM_BUILD_ROOT%{_libdir}
install sourceP/libcpdf.a $RPM_BUILD_ROOT%{_libdir}
#ln -sf %{name}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}.so.%{minorversion}
#ln -sf %{name}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}.so

install -d $RPM_BUILD_ROOT%{_fontsdir}/Type1/pfm
install fonts/*.pfb $RPM_BUILD_ROOT%{_fontsdir}/Type1
install fonts/*.pfm $RPM_BUILD_ROOT%{_fontsdir}/Type1/pfm
#cp fontmap.lst $RPM_BUILD_ROOT%{_datadir}/ghostscript/fonts

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -rf examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

gzip -9nf sourceP/*README* sourceP/ChangeLog doc/*.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc sourceP/*.gz doc/*.gz LICENSE*
%{_fontsdir}/Type1/*.pfb
%{_fontsdir}/Type1/pfm/*.pfm
#%{_datadir}/ghostscript/fonts/fontmap.lst
%attr(755,root,root) %{_libdir}/libcpdf.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcpdf.so
%{_includedir}/cpdflib.h
%{_examplesdir}/%{name}-%{version}
%doc doc/*.pdf

%files static
%defattr(644,root,root,755)
%{_libdir}/libcpdf.a
