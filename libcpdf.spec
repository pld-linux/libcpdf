Summary:	PDF manipulating library
Summary(pl):	Biblioteka do obrСbki plikСw PDF
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
Group(pt_BR):	Bibliotecas
Group(ru):	Библиотеки
Group(uk):	Б╕бл╕отеки
Source0:	http://www.fastio.com/clibpdf%{fileversion}.tar.gz
Source1:	%{name}-examples.Makefile
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-config.patch
URL:		http://www.fastio.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	zlib-devel
#Requires:	xpdf
#Requires:	ghostscript-fonts-std
#Requires:	ghostscript-fonts-other

%description
This is a library of ANSI C functions, for creating PDF files directly
via C.

%description -l pl
To jest biblioteka funkcji ANSI C do tworzenia plikСw PDF bezpo╤rednio
z C.

%package devel
Summary:	Header files needed for libcpdf development
Summary(pl):	Pliki nagЁСwkowe do programowania z u©yciem libcpdf
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name} = %{version}
Requires:	zlib-devel

%description devel
This package includes the header files for developing programs using
libcpdf.

%description devel -l pl
Ten pakiet zawiera pliki nagЁСwkowe potrzebne do programowania z
u©yciem libcpdf.

%package static
Summary:	Static libraries for libcpdf development
Summary(pl):	Statyczne biblioteki libcpdf
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name}-devel = %{version}
Requires:	zlib-devel

%description static
This package includes static libcpdf libraries.

%description static -l pl
Ten pakiet zawiera statyczne biblioteki libcpdf.

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
install sourceP/libcpdf.so* $RPM_BUILD_ROOT%{_libdir}
install sourceP/libcpdf.a $RPM_BUILD_ROOT%{_libdir}

#cp fontmap.lst $RPM_BUILD_ROOT%{_datadir}/ghostscript/fonts

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -rf examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

gzip -9nf sourceP/ChangeLog doc/*.txt fonts/README*

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc sourceP/*.gz doc/*.gz LICENSE*
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
