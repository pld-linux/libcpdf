Summary:   PDF manipulating library
Name:      libcpdf
Version:   2.02r1
%define    fileversion 202r1
%define    minorversion 2
Release:   0
URL:       http://www.fastio.com
Source0:   http://www.fastio.com/clibpdf%{fileversion}.tar.gz
Source1:   cpdfman110.pdf
Source2:   cpdfexamples.makefile
Source3:   afm2pfm.make
Patch0:    cpdfmakefile3.patch
Patch1:    cpdfconfig3.patch
Copyright: Free for non-commercial use
Group:     Libraries
BuildRoot: /tmp/%{name}-%{version}-root
Packager:  Gomez Henri <gomez@slib.fr>
Requires:  zlib
Requires:  xpdf
Requires:  ghostscript-fonts

%description
This is a library of ANSI C functions, for creating PDF files
directly via C.

%package devel
Summary:  header files and libraries needed for gd development
Group:    Development/Libraries
Requires: libcpdf = %{version}
Requires: zlib-devel

%description devel
This package includes the header files and libraries needed for
developing programs using clibpdf.

%prep
%setup -q -n ClibPDF
%patch0
%patch1

%build
cp $RPM_SOURCE_DIR/cpdfexamples.makefile examples/Makefile
cd sourceP
export CFLAGS="$RPM_OPT_FLAGS -DLinux -fPIC"
export VERSION="%{version}"
make -f Makefile.Linux shlib
export CFLAGS="$RPM_OPT_FLAGS -DLinux"
cd ../util/t1utils-1.9
./configure --prefix=$RPM_BUILD_ROOT/usr
make install
cd ../afm2pfm
cp $RPM_SOURCE_DIR/afm2pfm.make .
make -f afm2pfm.make
install -m 755 afm2pfm pfm2afm $RPM_BUILD_ROOT/usr/bin
install -m 644 README.afmpfm $RPM_BUILD_ROOT/doc


%install
cd sourceP
install -d $RPM_BUILD_ROOT/usr/{lib,include,bin,man/man1}
install -m 644 cpdflib.h $RPM_BUILD_ROOT/usr/include
install -m 755 %{name}.so.%{version} $RPM_BUILD_ROOT/usr/lib
install -m 644 %{name}.a $RPM_BUILD_ROOT/usr/lib
ln -sf %{name}.so.%{version} $RPM_BUILD_ROOT/usr/lib/%{name}.so.%{minorversion}
ln -sf %{name}.so.%{version} $RPM_BUILD_ROOT/usr/lib/%{name}.so
mkdir -p $RPM_BUILD_ROOT/usr/share/ghostscript/fonts/
cp *.pfm $RPM_BUILD_ROOT/usr/share/ghostscript/fonts
cp *.pfb $RPM_BUILD_ROOT/usr/share/ghostscript/fonts
cp fontmap.lst $RPM_BUILD_ROOT/usr/share/ghostscript/fonts


%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc sourceP/README* doc/*
/usr/bin/*
/usr/man/*
/usr/share/ghostscript/fonts/*.pfm
/usr/share/ghostscript/fonts/*.pfb
/usr/share/ghostscript/fonts/fontmap.lst
/usr/lib/%{name}.so.*
/usr/lib/%{name}.so

%files devel
%doc examples/ 
%defattr(-,root,root)
/usr/lib/%{name}.a
/usr/include/cpdflib.h

%changelog
* Tue Dec 14 1999 Gomez Henri <gomez@slib.fr>
- 2.02 Release 1
- Built under Redhat 5.2 with Type1 fonts in 
  /usr/share/ghostscript/fonts. Will be soon a
  release for Redhat 6.1 which use a different
  packaging of T1 fonts (urw-fonts)

* Tue Sep 14 1999 Gomez Henri <gomez@slib.fr>
- 2.00 Release 1

* Mon Sep 13 1999 Gomez Henri <gomez@slib.fr>
- 2.00Beta1 Release 2, major revision (thread support and API changes)
- first try
- libcpdfm.a and libcpdfm.so.xxx renamed to libcpdf.a and libcpdf.so.xxx

* Fri Jun 11 1999 Gomez Henri <gomez@slib.fr>
- 1.10-7e
- add Manual Addendum cpdfAdd110.pdf and included now cpdfman110.pdf
- correct makefile for examples

* Mon Jun  7 1999 Gomez Henri <gomez@slib.fr>
- correction in dynamic library build
- pdf viewer, xpdf, path to /usr/bin/X11/xpdf

* Wed May 5  1999 Gomez Henri <gomez@slib.fr>
- upgraded to version 1.10.5c

* Wed Mar 10 1999 Gomez Henri <gomez@slib.fr>
- initial release
- added shared library support
