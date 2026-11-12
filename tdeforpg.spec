%{!?pgmajorversion:%global pgmajorversion %(pg_config --version | sed -E 's/^[^0-9]*([0-9]+).*/\\1/')}
%{!?pginstdir:%global pginstdir /usr/pgsql-%{pgmajorversion}}

%global pname data_encryption
%global sname tdeforpg

%{!?llvm:%global llvm 1}
%{!?runselftest:%global runselftest 0}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name: %{sname}_%{pgmajorversion}
Version: 1.2.1.0
Release: 1%{?dist}
Summary: Transparent Data Encryption for PostgreSQL Free Edition
License: GPLv3
URL: https://github.com/tom-sato/%{sname}
Source0: https://github.com/tom-sato/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires: postgresql%{pgmajorversion}-devel
BuildRequires: postgresql%{pgmajorversion}-contrib
BuildRequires: chrpath
Requires: postgresql%{pgmajorversion}-server
Requires: postgresql%{pgmajorversion}-contrib
%if %runselftest
BuildRequires: postgresql%{pgmajorversion}-server pgdg-srpm-macros
BuildRequires: pgtap_%{pgmajorversion}
%endif

%description
Transparent Data Encryption for PostgreSQL is Encryption tool for PostgreSQL.
It adds encrypted data types to PostgreSQL.

%if %llvm
%package llvmjit
Summary: Just-in-time compilation support for tdeforpg
BuildRequires: llvm clang
Requires: %{name}%{_isa} = %{version}-%{release}
Requires: llvm

%description llvmjit
This package provides JIT support for tdeforpg
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}
chrpath -r '$ORIGIN' %{pname}.so

%install
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} install DESTDIR=%{buildroot}

%check
%if %runselftest
%pgdg_check_init
pgdg_check_start main "shared_preload_libraries = 'data_encryption'"
psql -X -v ON_ERROR_STOP=1 -d postgres \
-c "CREATE EXTENSION tdeforpg CASCADE" \
-c "SELECT cipher_key_disable_log()" \
-c "SELECT cipher_key_regist(NULL, '__replace__appropriate_encryption_key__', 'aes')" \
-c "CREATE EXTENSION pgtap"
pg_prove -d postgres -r SOURCES/test 
%endif

%files
%doc COPYRIGHT INSTALL-NOTE.TXT README RELEASE-NOTE.TXT UPGRADE-GUIDE.TXT
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}*.bc
%{pginstdir}/lib/bitcode/%{pname}/*.bc
%endif

%changelog
* Thu Nov 12 2026 Tomoaki Sato <tom-sato@sra.co.jp> - 1.2.1.0-1
- Initial packaging.
