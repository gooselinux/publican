
# Track font name changes
%define RHEL5 %(test %{?dist} == .el5 && echo 1 || echo 0)
%define RHEL6 %(test %{?dist} == .el6 && echo 1 || echo 0)
# Assume not rhel means FC11+ ... ugly
%define OTHER 1
%if %{RHEL6}
%define OTHER 0
%endif
%if %{RHEL5}
%define OTHER 0
%endif

# who doesn't have xdg-open?
%define HTMLVIEW %(test %{RHEL5} == 1 && echo 1 || echo 0)

# required for desktop file install
%define my_vendor %(test %{OTHER} == 1 && echo "fedora" || echo "redhat")

%define TESTS 0

Name:           publican
Version:        2.1
Release:        0%{?dist}
Summary:        Common files and scripts for publishing with DocBook XML
# For a breakdown of the licensing, refer to LICENSE
License:        (GPLv2+ or Artistic) and CC0
Group:          Applications/Publishing
URL:            https://publican.fedorahosted.org
Source0:        https://fedorahosted.org/released/publican/Publican-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Limited to these arches on RHEL 6 due to PDF + Java limitations
%if %{RHEL6}
BuildArch:      i386 x86_64
%else
BuildArch:      noarch
%endif

# Get rid of the old packages
Obsoletes:      perl-Publican-WebSite < 1.5
Obsoletes:      publican-WebSite-obsoletes < 1.21
Provides:       perl-Publican-WebSite = 1.5
Provides:       publican-WebSite-obsoletes = 1.21

BuildRequires:  perl(Devel::Cover)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Perl::Critic)
BuildRequires:  perl(Archive::Tar)
BuildRequires:  perl(Archive::Zip)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config::Simple)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(DateTime::Format::DateParse)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Copy::Recursive)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::pushd)
BuildRequires:  perl(HTML::FormatText)
BuildRequires:  perl(HTML::TreeBuilder)
BuildRequires:  perl(I18N::LangTags::List)
BuildRequires:  perl(Image::Magick)
BuildRequires:  perl(Image::Size)
BuildRequires:  perl(Locale::Maketext::Gettext)
BuildRequires:  perl(Locale::Language)
BuildRequires:  perl(Locale::PO)
BuildRequires:  perl(Makefile::Parser)
BuildRequires:  perl(Syntax::Highlight::Engine::Kate)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(Text::Wrap)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(version)
BuildRequires:  perl(XML::LibXML)  >=  1.67
BuildRequires:  perl(XML::LibXSLT) >=  1.67
BuildRequires:  perl(XML::TreeBuilder) >= 3.09-15
BuildRequires:  fop >= 0.95
BuildRequires:  batik
BuildRequires:  docbook-style-xsl >= 1.75.2-5
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  perl-Template-Toolkit
BuildRequires:  perl(DBD::SQLite)

# Most of these are handled automatically
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Locale::Maketext::Gettext)
Requires:       fop >= 0.95
Requires:       batik rpm-build
Requires:       docbook-style-xsl >= 1.75.2-5
Requires:       perl(XML::LibXML)  >=  1.67
Requires:       perl(XML::LibXSLT) >=  1.67
Requires:       perl(XML::TreeBuilder) >= 3.09-15
Requires:       gettext cvs
Requires:       perl-Template-Toolkit
Requires:       perl(DBD::SQLite)

# Pull in the fonts for all languages, else you can't build translated PDF in brew/koji
%if %{RHEL5}
Requires:       fonts-bengali fonts-chinese fonts-chinese-zysong fonts-gujarati
Requires:       fonts-hindi fonts-japanese fonts-kannada fonts-korean
Requires:       fonts-malayalam fonts-oriya fonts-punjabi fonts-sinhala
Requires:       fonts-tamil fonts-telugu liberation-fonts
BuildRequires:  fonts-bengali fonts-chinese fonts-chinese-zysong fonts-gujarati
BuildRequires:  fonts-hindi fonts-japanese fonts-kannada fonts-korean
BuildRequires:  fonts-malayalam fonts-oriya fonts-punjabi fonts-sinhala
BuildRequires:  fonts-tamil fonts-telugu liberation-fonts
#BuildRequires:  java-1.5.0-sun java-1.5.0-sun-devel chkconfig
%endif
%if %{RHEL6}
Requires:       liberation-mono-fonts liberation-sans-fonts liberation-serif-fonts
Requires:       cjkuni-uming-fonts ipa-gothic-fonts ipa-pgothic-fonts
Requires:       lklug-fonts baekmuk-ttf-batang-fonts

BuildRequires:  liberation-mono-fonts liberation-sans-fonts liberation-serif-fonts
BuildRequires:  cjkuni-uming-fonts ipa-gothic-fonts ipa-pgothic-fonts
BuildRequires:  lklug-fonts baekmuk-ttf-batang-fonts
%endif
%if %{OTHER}
Requires:       liberation-mono-fonts liberation-sans-fonts liberation-serif-fonts
Requires:       cjkuni-uming-fonts ipa-gothic-fonts ipa-pgothic-fonts
Requires:       lklug-fonts baekmuk-ttf-batang-fonts

BuildRequires:  liberation-mono-fonts liberation-sans-fonts liberation-serif-fonts
BuildRequires:  cjkuni-uming-fonts ipa-gothic-fonts ipa-pgothic-fonts
BuildRequires:  lklug-fonts baekmuk-ttf-batang-fonts
%endif

Obsoletes:      Publican < 1.0
Provides:       Publican = 1.0

%description
Publican is a DocBook publication system, not just a DocBook processing tool.
As well as ensuring your DocBook XML is valid, publican works to ensure
your XML is up to publishable standard.

%package doc
Group:          Documentation
Summary:        Documentation for the Publican package
%if %{HTMLVIEW}
Requires:       htmlview
%else
Requires:       xdg-utils
%endif
Obsoletes:      Publican-doc < 1.0
Provides:       Publican-doc = 1.0

%description doc
Publican is a tool for publishing material authored in DocBook XML.
This guide explains how to  to create and build books and articles
using publican. It is not a DocBook XML tutorial and concentrates
solely on using the publican tools.

%prep
%setup -q -n Publican-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build
dir=`pwd` && cd Users_Guide && perl -I $dir/blib/lib $dir/blib/script/publican build \
        --formats=html-desktop --publish --langs=all \
        --common_config="$dir/blib/datadir" \
        --common_content="$dir/blib/datadir/Common_Content"

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

./fop-ttc-metric.pl --outdir $RPM_BUILD_ROOT%{_datadir}/publican/fop/font-metrics --conffile $RPM_BUILD_ROOT%{_datadir}/publican/fop/fop.xconf

sed -i -e 's|@@FILE@@|%{_docdir}/%{name}-doc-%{version}/en-US/index.html|' %{name}.desktop
sed -i -e 's|@@ICON@@|%{_docdir}/%{name}-doc-%{version}/en-US/images/icon.svg|' %{name}.desktop

%if %{HTMLVIEW}
sed -i -e 's|xdg-open|htmlview|' %{name}.desktop
%endif

desktop-file-install --vendor="%{my_vendor}" --dir=$RPM_BUILD_ROOT%{_datadir}/applications %{name}.desktop

for file in po/*.po; do
	lang=`echo "$file" | sed -e 's/po\/\(.*\)\.po/\1/'`;
        mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/$lang/LC_MESSAGES;
	msgfmt $file -o $RPM_BUILD_ROOT%{_datadir}/locale/$lang/LC_MESSAGES/%{name}.mo;
done

%find_lang %{name}

%check
%if %{TESTS}
./Build test
%endif
%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc CHANGES README COPYING Artistic
%{perl_vendorlib}/Publican.pm
%{perl_vendorlib}/Publican/*
%{_mandir}/man3/Publican*
%{_mandir}/man1/*
%{_bindir}/publican
%{_datadir}/publican
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/publican-website.cfg

%files doc
%defattr(-,root,root,-)
%doc Users_Guide/publish/desktop/*
%{_datadir}/applications/%{my_vendor}-%{name}.desktop
%doc fdl.txt

%changelog
* Tue Jul 06 2010 Jeff Fearn <jfearn@redhat.com> 2.1-0
- Fix broken install_book not updating DB.
- Fix typos in docs.

* Tue Jul 06 2010 Jeff Fearn <jfearn@redhat.com> 2.0-0
- Add Publican::Website.
- Add web_*_label params for web menus.
- Add underscores to cleanset, installbrand, and printtree. BZ #581090
- Update docs with Website content
- Update brand license text.
- Fix different log jar path on F14+
- Add constraint to help_config output.
- Fix segfault when indexterm has no leading content. BZ #592666
- Fix inline indexterm. BZ #592823
- Translate productname tag. BZ #592669
- Fix formalpara missing ID. BZ #595564
- Add dummy lang.css to avoid 404's. BZ #595799
- Improve validation error message. BZ #593887
- Fix qandaentry ID. BZ #593892
- Fix Icon non-conformance. BZ #593890
- Fix admonitions splitting across pages. BZ #596257
- Fix HTML simple list border. BZ #599258
- Fix formal object IDs. BZ #601363
- Fix Revision History layout. BZ #559787 #598828 #598833
- Remove title color from term in HTML. BZ #592822
- Fix highlight breaking callouts. BZ #590933
- Add support for LineColumn coords in area tag.
- Update font requires for F12 and F13.
- Fix clean_ids adding newline to verbatim. BZ #604465
- Fix index missing ID. BZ #606418
- Fix files dir being missed. BZ #609345
- Adjust admonition layout.

* Wed May 12 2010 Jeff Fearn <jfearn@redhat.com> 1.6.3-0
- Disable verbatim hyphenation. BZ #577068
- Fix anchors breaking HTML. BZ #579069
- Fix common options not in help text.
- Fix formatting of abstract in spec. BZ #579928
- Translate verbatim tags. BZ #580360
- Add print_unused option. BZ #580799
- Overwrite zero length PO files. BZ #581397
- Fix citerefentry breaking translation. BZ #581773
- Fix reference bug in html-single.
- Added print_known and print_banned actions.
- Fix typo in POD. Raphaël Hertzog <hertzog@debian.org>
- Fix indexterm translation. BZ #582255
- Fix non-breaking space being treated like normal white space. BZ #582649
- Fix webkit & pdf table borders. BZ #585115
- Make indexterm translatable. BZ #582680
- Make keyword translatable. BZ #583224
- Add Eclipse help target. BZ #587489
- Convert MAX_WIDTH to a parameter max_image_width. BZ #580774
- Add confidential text to title, first, and blank pages in PDF. BZ #588980
- Add confidential_text parameter. BZ #588980
- Fix article list formatting in HTML. BZ #588999
- Fix epub validation issues. BZ #589333
- Fix xref to term with indexterm BOOM. BZ #580751
- Fix keyword highlight breaking callouts. BZ #590933
- Fix right icon misaligned. BZ #590964

* Thu Apr 01 2010 Jeff Fearn <jfearn@redhat.com> 1.6.2-0
- Fix hyphenate.verbatim running out of depth. BZ #577095
- Fix UTF8 error in translations. BZ #576771
- Add surname and othername to translatable tag list. BZ #578343
- No fuzzy strings in merged XML. BZ #578337
- Allow clean_ids to add entity reference. BZ #576462
- Added --quiet and --nocolours. BZ #578366

* Mon Mar 22 2010 Jeff Fearn <jfearn@redhat.com> 1.6.1-0
- Fix package_brand including unwanted files. BZ #570715
- Fix empty lines breaking callouts. BZ #570046
- Detect verbatim content in translatable content. BZ #571633
- Fix missing IO::String requires properly. BZ #568950
- Add print style sheet to XHTML. RT #60327
- Force UTF8 on all files. BZ #570979
- Fix comments in callout breaking build. BZ #572047
- Fix table border display. BZ #572995

* Mon Mar 01 2010 Jeff Fearn <jfearn@redhat.com> 1.6-0
- Fix missing IO::String requires. BZ #568950
- Fix xml_lang error. BZ #569249

* Fri Feb 26 2010 Jeff Fearn <jfearn@redhat.com> 1.5-0
- Croak if profiling would remove root node.
- Add Archive::Zip to Build.pl
- Fix --config and add to help text
- Force footnotes and indexterms to be inline for translations. BZ #563056
- Add CVS package option. RT #59132
- Fix white space issues in abstract. BZ #559823
- Fix translation strings not matching correctly BZ #563397
- Fix entity with underscore. BZ #561178
- Fix config values of zero being ignored. BZ #564405
- Fix footnote number missing in footer. BZ #565903
- Fix duplicate text in callouts. BZ #561618
- Remove outdated references to catalogs parameter. BZ #565498
- Fix white space in book name breaking creation.
- Fix nested tag with similar name breaking translation. BZ #568201
- Fix translated packages using source version.
- Switch from object to iframe BZ #542524
- More accurate word counts for translations reports.

* Fri Jan 29 2010 Jeff Fearn <jfearn@redhat.com> 1.4-1
- make font BuildRequires match requires.

* Mon Jan 25 2010 Jeff Fearn <jfearn@redhat.com> 1.4-0
- Ignore obsolete entries in stats code. BZ #546130
- Fix valid_lang matching on unknown languages.
- Fix invalid tag in DTD. BZ #548629
- Added contrib to translation tag list. BZ #550460
- Added firstname, lastname, orgname to translation tag list. BZ #555645
- Remove comments from translations. BZ #555647
- Fix content in root nodes not being added to pot. BZ #554261
- Fix mixed mode content being dropped when merging translations. BZ #549925
- Fix ID creation in refentry. BZ #553085
- Add gettext Requires. BZ #550461
- Fix non-default tmp dir. BZ #551974
- Fix validation output. BZ #556684
- Fix tag attributes breaking translation merge. BZ #554230
- Format XML when running create. BZ #556201
- Switch Japanese font to ipa-gothic-fonts on Fedora.
- Fix Japanes mono/proportional font selection.
- Add TTC build time script. BZ #557336
- Add check for main file before parsing.
- Add check for OS before running FOP.

* Tue Dec 08 2009 Jeff Fearn <jfearn@redhat.com> 1.3-0
- Fixed --version BZ #533081
- Fixed empty params in new book cfg file. BZ #533322
- Fixed clean_ids taking too long.
- Added nowait option for brew.
- Improved epub support. BZ #536706
- Add missing rpm-build req. BZ #537970
- Changed ol ol style. BZ #537256
- Fix missing revision history field crash. BZ #539741
- Fix bug in condition logic in XmlClean. BZ #540685
- Add translation stats. BZ #540696
- Stopped processing xml files in extras dir. BZ #540383
- Fixed callout rendering. BZ #531686
- Fix wrong docs for condition usage. BZ #540691
- Remove list style from stepalternatives. BZ #511404
- Force step::para to keep-with-next if followed by a figure.
- Edited Conventions.xml.
- Exclude Legal_Notice.xml from pot creation.
- Fix nested XML breaking translations.
- Fix syntax highlighting adding whitespace. BZ #544141
- Better error message for Kate language mismatch.

* Wed Nov 4 2009 Jeff Fearn <jfearn@redhat.com> 1.2-0
- Fix images missing from distributed set output. BZ #532837
- Correct image path when running clean_ids.
- Fix typo in format description. BZ #532379
- Add comment to clean.
- force package to run clean to avoid stale content. BZ #538676

* Mon Nov 2 2009 Jeff Fearn <jfearn@redhat.com> 1.1-0
- Fix brew failure. BZ #532383
- Fix distributed sets no packaging properly.

* Mon Oct 26 2009  Jeff Fearn <jfearn@redhat.com> 1.0-0
- Add base langauge summary & descriptions to translated spec file. BZ #515573
- Fix translated package build failure.
- Change tabs to spaces in generated spec files.
- Fix Locale::Maketext::Gettext dep being missed on RHEL.
- Fix common paths on Windows
- Added docbook-style-xsl dep for version 1.75.1+
- POD fix from Mikhail Gusarov <dottedmag@dottedmag.net>
- Added processing file message to update_pot. BZ #518354
- add EPUB stub
- Clean up Copyright in numerous files.
- Add security callback for exslt:document.
- Update XML::LibXML & XML::LibXSLT minimum versions to 1.67
- Fix rounded corners in HTML. BZ #509768
- Fix nested images breakin in PDF. BZ #491782
- Remove border from HTML table for simplelist. BZ #502126
- Fix remarks not being highlighted in PDF. BZ #509307
- Resize shade.verbatim font size. BZ #497462
- Change step page size limitation to para size limitation. BZ#492984
- Add warning message for missing images. BZ #495821
- Fix fuzzy images. BZ #479794
- swap from paths from Publican to publican and obsolete beta packages.
- Fix large example PDF issue. BZ #531685

* Sat Jul 18 2009  Jeff Fearn <jfearn@redhat.com> 0.99-0.ALPHA1
- Rebase to Perl rewrite.

* Wed Mar 25 2009 Jeff Fearn <jfearn@redhat.com> 0.45
- Add keep-together.within-column="always" to step. BZ #492021
- Fix right to left fo ar-AR. BZ #486162
- Patches and translations by Muayyad Alsadi <alsadi@ojuba.org> 
- Added missing doccomment and number to PDF highlight. BZ #491241
- Fix files dir missing from RPMs. BZ #492034

* Wed Mar 11 2009  Jeff Fearn <jfearn@redhat.com> 0.44
- Add 0-9 and '.' to DOCNAME regex. BZ #489626

* Mon Mar 9 2009  Jeff Fearn <jfearn@redhat.com> 0.43
- Fix many warnings about 'body-start() called from outside an fo:list-item' BZ #484628
- Fix Initial build of new lang failing. BZ #485179
- Add lang to final doc root node. BZ #486162
- Add embed for stanky IE. BZ #486501
- Add symlinks for langauges without country codes. BZ #487256
- Add rudimentary Obsoletes logic. RT #36366
- Rolled in following from fedora devel spec
- - Mon Feb  9 2009 Jens Petersen <petersen@redhat.com> - 0.40-4
- - update the sazanami-fonts subpackage names
- - list liberation-fonts subpackages explicitly
- - Fri Feb  6 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.40-3
- - Fix broken font deps: liberation-fonts -> liberation-fonts-compat
- - Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> - 0.40-2
- - cjkunifonts-uming -> cjkuni-uming-fonts
- - Thu Jan 22 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.40-1
- - Font changes baekmuk-ttf-fonts-batang -> baekmuk-ttf-batang-fonts to
-   fix broken deps in rawhide
- Fri Mar 6 2009 Piotr Drąg <piotrdrag@gmail.com>
- Translate Document Conventions into Polish
- Thu Mar 5 2009 Piotr Drąg <piotrdrag@gmail.com>
- Translate common Feedback section into Polish
- Wed Mar 4 2009 Richard van der Luit <zuma@xs4all.nl>
- Corrections to Document Conventions in Dutch
- Mon Mar 2 2009 Richard van der Luit <zuma@xs4all.nl>
- Translate Document Conventions into Dutch
- Sat Feb 28 2009 Rui Gouveia <rui.gouveia@globaltek.pt>
- Translate Document Conventions into European Portuguese



* Thu Jan 29 2009 Jeff Fearn <jfearn@redhat.com> 0.42
- Support chapterinfo, keywordset & keyword tags.
- Add SRC_URL. BZ #482968
- Fix web package removal when dep package has been removed.

* Mon Jan 19 2009 Jeff Fearn <jfearn@redhat.com> 0.41
- Fix Source tar name.
- Fix brew srpm path
- Added OS_VER to allow over ride of OS srpm is created for.

* Mon Jan 5 2009 Jeff Fearn <jfearn@redhat.com> 0.40
- Fix DRAFT mode in web docs.
- Fix TOC CSS spacing.
- Fix missing syntax highlighting templates. BZ #474077
- Added appendix to user guide for Makefile parameters. BZ #476913
- Fix multiple authors in revhistory. Patch by: Paul W. Frields. BZ #478552
- Add LICENSE override for RPMs. BZ #477720
- Fix empty change log. BZ #477728
- Fix spec file location. BZ #477704
- Added newline after country. BZ #477573
- Fix minimum font size breaking TOC. BZ #476884
- Fix missing font-metric files. BZ #479592
- Updated redhat brand license. BZ #478405
- Update jboss brand license. BZ #478416
- Ship PDF with Indic web packages.

* Mon Dec 1 2008 Jeff Fearn <jfearn@redhat.com> 0.39
- Disable make.graphic.viewport. BZ #467368
- Add missing XEP namespace. BZ #467256
- Add catch for ValidateTables where table for tgroup could not be found. BZ #468789
- Fix right margin error on verbatim and admonitions in PDF. BZ #467654
- Added foreignphrase to list of validated tags.
- Add foreignphrase, acronym, hardware to list of tags aspell should ignore.
- Fixed left align of verbatim items in notes.
- Fixed contrib class in CSS. BZ #469595
- Changed para & simpara to div in HTML. BZ #469286
- Fix layout of author in Revision History. BZ #469986
- Validated function tag. BZ #471144
- Fixed menu entry text. BZ #470967
- Validated type, methodname, excAppendix.xmleptionname, varname, interfacename tags. BZ #461708
- Banned glosslist (untranslatable) BZ #461864
- Validated uri, mousebutton, hardware tags. BZ #461870
- Validated othername tag. BZ #464315
- Removed collab from front page to match PDF output. BZ #469298
- Formalised handling of draft mode, root node only. BZ #468305
- Removed old help text from create_book and make type case insensitive. BZ #471776
- Fixed footnote numbers collapsing together. BZ #462668
- Fix translation report for po in nested directories.
- Changed Formal Para Title to follow parent indent. BZ #466309
- Validated qandadiv, tweaked layout. BZ #472482
- Handle xslthl:annotation. BZ #472500
- Fix dot on docnav css. BZ #472627
- Fix ol display in article. BZ #472491
- Added section of Drafting rules. (bforte)
- Fix CCS display of image in term.
- Add product URL. Modify header to use product url.
- Fix formalpara missing div. BZ #473843
- Fix OL missing margin in article. BZ #473844

* Thu Oct 16 2008 Jeff Fearn <jfearn@redhat.com> 0.38
- Fix inline tags removing following new line in verbatim tags. BZ #461369
- Fix Numeration settings for HTML ordered lists. BZ #462601
- Fix PDF Example background color. BZ #463127
- Fix list item spacing. BZ #462673
- Fix translation report error on 2 charater langs, CSS, and layout. BZ #465201
- Added error for tgroup.cols not matching entry count. BZ #462205
- Fix TOC padding for appendix and glossary. BZ #462991
- Made comments in highlighted code more prominent. BZ #462552
- Added citerefentry, refentrytitle, and manvolnum to list of QA'd tags. BZ #464038
- Fixed '1' in ulink with no text. BZ #465411
- Change env path to be more portable. Patch by Artem Zolochevskiy . BZ #466194
- Added package meta to XHTML to allow content to be tracked to an RPM.
- Added catch for missing title and productname.
- Changed Formal Para Title to follow parent indent. BZ #466309
- Fix xmlClean not handling entity names with underscores or numbers. BZ #466994
- Fix clean_ids removing comments. BZ #467145
- Fix missing revhistory giving useless error. BZ #467147
- Stopped proecssing xml files in extras directory.
- Added conditional tagging to user Guide. By Don Domingo.

* Wed Sep 3 2008 Jeff Fearn <jfearn@redhat.com> 0.37
- Fix Bug in web rpm upgrade script.
- Fix Article not building rpms.
- Switch ja-JP  font name in pdf from SazanamiMincho to SazanamiGothic
- Remove empty para tags to break en-US HTML build so writers stop breaking translations.
- Changed docs reference from --revision to --edition for create_book option
- Fixed Article layout not matching Book Layout. BZ #460969
- Fixed Part not ledded properly in TOC BZ #460976
- Fix duplicate IDs in XHTML output.
- Made background of remark a pretty yellow. BZ #459213
- Fix Accessibility typo. BZ #460856
- Fix spurious hyphenation in verbatim.
- Fix broken RPM packages when titles have been translated.
- Fix display bug in html-single. BZ #461375
- Added FAQ entry for Java weirdness. BZ #460738
- Add default encoding to XML files. BZ #461379
- Removed corpauthor from template. BZ #461222
- Fixed create_book help text. BZ #460736
- Added menuchoice tag. BZ #459671
- Removed unused scripts entity2pot and po2entity

* Mon Sep 1 2008 Jeff Fearn <jfearn@redhat.com> 0.35-0
- Add missing xerces-j2 Requires. BZ #457497
- Fixed css path for tranlation reports.
- Fixed font path for Fedora, ensured build fails if font metric creation fails. BZ #458003
- Set vertical-align:top for TD - BZ #457851
- Added WARNING for ENTITIES declared in XML files. BZ #456170
- Added check to ensure PRODUCT has a valid format.
- Only check xml files for revision history. BZ #458740
- Made VERSION and RELEASE over-rideable. BZ #458421
- Fixed display of OL nested in UL. BZ #457915
- Added "make pom" to output a basic maven pom file.
- Updated doco. BZ #458764
- Updated Conventions.xml. BZ #456026 #459216
- Made PDF and HTML display product version in similar style. BZ #456486
- Remove ID's from common files. BZ #460770
- Allowed footnote to keep ID. BZ #460790
- Fixed bogus verbatim layout. BZ #460771

* Fri Apr 11 2008 Jeff Fearn <jfearn@redhat.com> 0.34-0
- Fix PO file name missing from translation status report
- Modify xmlClean to output dummy content for empty files (beta)
- Default SHOW_UNKNOWN tags off
- Make unset entity warnings more obvious
- Make docs use DESKTOP styles
- Fix missing list image in html-single articles
- Commented out debug output in chunking xsl
- QANDA set html and css fix BZ #442674
- Fix kde requires. BZ #443024
- Add default FOP xconf file.
- Added help_internals target.
- Added check for banned tags.
- Added --lang to create_book BZ #444851
- Added package tag BZ #444908
- Added ability to ship $lang/files directories with html/xml payloads BZ #444935
- Hardcoded PDF footnote colour to black BZ #446011
- Set segmentedlist.as.table to 1. BZ #445628
- Force monospace on command
- Switched to FOP 0.95Beta
- Fixed crash bug on files names with parentheses BZ #447659
- Fix loose directory name matching when exluding directiories.
- Added GENERATE_SECTION_TOC_LEVEL to allow section level TOC control. BZ #449720
- Banned inlinegraphic. BZ #448331
- Added Article and Set Templates
- Banned xreflabel and endterm. BZ #452051
- Generate FOP config file and font-metricfiles as build. BZ #451913
- Changed HTML and PDF common brand to more pleasing colors. BZ #442675 
- Fixed incorrect PDF colours on Fedora and Common brands. BZ #442988
- Fixed PDF TOC missing Chapter numbers on Sections. BZ #452802
- Fixed spaces being removed between inline tags. BZ #453067
- Changed TOC layout (bold chapters + spacing). BZ #453885
- Changed title spacing, unbolded figure/table titles.
- Fix over size images breaking PDF and HTML layouts
- Add missing make Requires. BZ #454376
- Added call to aspell to spell check.
- Fixed incorrect other credit title in PDF. BZ #454394
- Turned on Hyphenation to split verbatim lines.
- Added code highlighting to CSS and PDF
- Remove trailing '.' from formal para title. BZ #455826
- Restructure CSS for easier maintenance of brands
- Add documentation on publican design philosophy. BZ #456170
- Italicised package tag. BZ #442668
- Updated documentation descriptions of Book_Info.xml tags. BZ #456489 BZ #456488


* Mon Apr 7 2008 Jeff Fearn <jfearn@redhat.com> 0.33-0
- Remove release from package name in html desktop spec file
- Removed --nonet from xsltproc call BZ #436342
- Add Desktop css customisations

* Thu Apr 3 2008 Jeff Fearn <jfearn@redhat.com> 0.32-0
- Bump version

* Tue Mar 18 2008 Jeff Fearn <jfearn@redhat.com> 0.31-0
- Fixed Project-Id-Version not being set on PO creation BZ #435401
- Fixed java slowing down every make run BZ #435407
- cleanIds now sets format for imagedata
- Fixed Desktop RPM build errors
- Added param DOC_URL BZ #437705
- Changed Default DOC_URL to publican web site
- Fixed perl-SGML-Translate file conflict
- Removed --nonet from xsltproc call BZ #436342
- Removed extra files logic from spec and xsl files.

* Thu Feb 24 2008 Jeff Fearn <jfearn@redhat.com> 0.30-0
- Added missing Requires perl(XML::TreeBuilder)
- Fix xref to listitem breaking BZ #432574
- Die with a decent warning when an invalid Brand is chosen. BZ #429236
- Modified title page of PDF. BZ #429977
- Fix PDF list white space issue BZ #429237
- Fix PDF ulinks too big for tables BZ #430623
- Allowed rev history to be in any file BZ #297411
- Fix keycap hard to read in admon BZ #369161
- Added per Brand Makefile
- Add per Brand xsl files
- Added Requires elinks (used for formatted text output)
- Handle different FOP versions
- Fix PDF issue with nested images
- Added id_node to clean_ids to use none title nodes for id's BZ #434726
- Fix footnotes being duplicated in wrong chunks BZ #431388
- fixed bold text CSS bug for BZ #430617

* Wed Feb 13 2008 Jeff Fearn <jfearn@redhat.com> 0.29-2
- replace tab in changelog with spaces

* Tue Feb 12 2008 Jeff Fearn <jfearn@redhat.com> 0.29-1
- removed %%post and %%postun as update-desktop-database is
-   for desktop files with mime types
- removed release for source path and tar name
- fixed package name in desktop file to include -doc
- switched from htmlview to xdg-open
- Added xdg-utils requires for doc package

* Tue Feb 12 2008 Jeff Fearn <jfearn@redhat.com> 0.29-0
- Setup per Brand Book_Templates
- Fix soure and URL paths
- Use release in source path
- correct GPL version text and changed file name to COPYING
- dropped Provides
- reordered spec file
- added fdl.txt to tar ball.
- added fdl.txt to doc package

* Mon Feb 11 2008 Jeff Fearn <jfearn@redhat.com> 0.28-0
- Added gpl.txt
- Fix GPL identifier as GPLv2+
- Fixed Build root
- Fix desktop file
- Added Provides for documentation-devel
- Fix dist build target
- Add dist-srpm target
- fix dist failing on missing pot dir
- Put docs in sub package
- Added GFDL to License to cover content and Book_Template directories.
- Included GFDL txt file
- set full path to source

* Thu Feb 07 2008 Jeff Fearn <jfearn@redhat.com> 0.27-0
- Use docbook-style-xsl: this will break formatting.
- Update custom xsl to use docbook-xsl-1.73.2: this will break formatting.
- Remove CATALOGS override
- Remove Red Hat specific clause from Makefile.common
- Fixed invalid xhtml BZ 428931
- Update License to GPL2
- Add GPL2 Header to numerous files

* Fri Feb 01 2008 Jeff Fearn <jfearn@redhat.com> 0.26-5
- renamed from documentation-devil to publican

* Thu Jan 17 2008 Jeff Fearn <jfearn@redhat.com> 0.26-4
- Tidy up %%files, %%build, %%prep and remove comments from spec file.
- Added --atime-preserve to tar command

* Mon Jan 07 2008 Jeff Fearn <jfearn@redhat.com> 0.26-3
- Rename from documentation-devel to documentation-devil

* Mon Jan 07 2008 Jeff Fearn <jfearn@redhat.com> 0.26-2
- tidy spec file

* Wed Jan 02 2008 Jeff Fearn <jfearn@redhat.com> 0.26
- Added CHUNK_SECTION_DEPTH param to allow chunk.section.depth override. BZ #427172
- Fixed EXTRA_DIRS to ignore .svn dirs, Added svn_add_po target. BZ #427178
- Fixed "uninitialized value" error when product not set. BZ #426038
- Fixed Brand not updating. BZ #426043
- Replaced FORMAL-RHI with HOLDER in Book_Template. BZ #426041
- Remove reference to non-existant svg file. BZ #426063
- Override formal.title.properties for PDF. BZ #425894
- Override formal.object.heading for HTML. Fix H5 & H6 css. BZ #425894
- Prepended first 4 characters of tag to IDs to aid Translation. BZ #427312

* Tue Dec 11 2007 Jeff Fearn <jfearn@redhat.com> 0.25
- Add html.longdesc.embed xsl param to allow long descriptions of images to be embedded in html output
- Remove Boilerplate files as ther are dupes of Legal_Notice
- Added BRAND Makefile param to allow branding books.
- renamed redhat.xsl to defaults.xsl
- Fixed product not being updated in Makefile when using create_book BZ #391491
- Removed embedded font from English PDFs as it Breaks searching
- Added user documentation
- create_book: fixed version and revision not working
- Added dist target to create tar & spec files for desktop rpms
- Made desktop rpms use html-single BZ #351731
- Removed gnome-doc-utils dep
- Removed docbook-style-xsl dep
- Removed perl-SGML-Translate dep
- Removed unused Config::Simple module
- Switch from Template to HTML::Template as it's already in Fedora
- Switched xlf2pot from XML::SimpleObject to XML::TreeBuilder
- Added error messages for invalid VERSION or RELEASE
- Changed Default PRODUCT to Documentation
- Added warning for default PRODUCT
- Differentiated brands
- rename rhlogo.png title_logo.png
- removed unused images
- cleaned build process

* Tue Nov 6 2007 Jeff Fearn <jfearn@redhat.com> 0.24
- Fix bug with calling translation report script.

* Mon Nov 5 2007 Jeff Fearn <jfearn@redhat.com> 0.23
- Add postuff to validate po files
- Add test-po-<LANG> targets to use po-validateXML from postuff
- Fixed error msgs in poxmerge
- Fix bug with directory creation for deeply nested po files
- Fixed bug where Common files could not access <bookname>.ent file BZ #322721
- Add entity for root using <systemitem class='username'>
- Added create_book command and files to allow local creation of new books
- Added SHOW_REMARKS make param to control display of remark tags
- Added OASIS dtd in xml for Kate users
- Sort image list for bin/rmImages to aid readability
- Modified padding and margins between figures and their titles
- Added DejaVuLGCSansMono font metrics
- Added DejaVuLGCSans Oblique metrics
- Added missing dejavu-lgc-fonts dep
- Added build message when copying Product Specific common files
- Move local entity to first position so it overrides common entity files
- Added missing DocBook tags to xmlClean:
-         accel blockquote classname code colophon envar example footnote
-         guisubmenu interface keycap keycombo literal literallayout option
-         parameter prompt property see seealso substeps systemitem wordasword
-         glossary glossdiv glosssee glossseealso
- Moved executables in to bin directory.
- Fixed layout of formal para titles in PDF
- Removed trunctaion and elipses from title used for page headers

* Wed Oct 3 2007 Jeff Fearn <jfearn@redhat.com> 0.22
- Add handling of extras directory
- Fix Russian PDF font problem

* Tue Sep 25 2007 Jeff Fearn <jfearn@redhat.com> 0.21
- Modified screen and programlisting to force closing tag to be on it's own.
- Added cmdsynopsis, arg, articleinfo, article, informaltable, group to xmlClean.
- Added CHUNK_FIRST to allow per book control of first section chunking.
-  Defaults to 1, first sections will be on their own page.
- Fix warning message on po files with no entries
- added role as class to orderedlist, itemizedlist, ulink, article
- Fixed po files in sub directories not being merged correctly
- Add website specific css

* Tue Aug 28 2007 Jeff Fearn <jfearn@redhat.com> 0.20
- Added IGNORED_TRANSLATIONS to allow users to replace the chosen languages with
-  the default langauge text when building
- fix bug where build would fail if $(XML_LANG)/images did not exist
- Fix bug with rpm downgrade
- fixed CSS bug for preformatted text when rendered inside inside an example.

* Tue Aug 28 2007 Jeff Fearn <jfearn@redhat.com> 0.19
- Add missing targets to help output
- Add missing variables to help_params output
- Improve help and help_params text
- Changed entity RHCRTSVER to 8.0 from 7.3
- Add DejaVuLGCSans back as Liberation is broken and Russian requires DejaVuLGCSans
- Modify Makefile to pull PO files from translation CVS
- Ensure Legal_Notice.po[t] is never used
- Add a warning message for GUI_String update-pot
- Fix Bug in GUI String publish targets
- Converted reports from hard coded HTML to Templates
- Publish GUI_String translation reports to same location as documentation reports.

* Thu Aug 16 2007 Jeff Fearn <jfearn@redhat.com> 0.18
- Use ghelp to enable localised menus (BZ #249829)
- Fix broken if in subpackage.xsl
- Fix Icon missing from menu

* Mon Aug 13 2007 Jeff Fearn <jfearn@redhat.com> 0.17
- Remove unused PUB_DIR make variable
- Remove 'redhat-' from FOP common paths
- Improve help text.
- Add error message for trying to build language without po files
- Added error message for trying to report on a language with no PO files
- Added error message for trying to build reports without POT files

* Fri Jun 29 2007 Jeff Fearn <jfearn@redhat.com> 0.16
- Added img.src.path to admon.graphics.path
- Moved header.navigation and footer.navigation from xhtml-common to main-html
- Removed 'redhat' from name
- Remove NOCHUNK param, Added html-single targets
- Added eclipse support
- removed xmlto Requires
- added Legal_Notice.xml for future books. Boilerplate.xml remains for back compatibility.
- Fix rpm link creation
- Added creation of format specific rpms
- Added rmImages script to remove unused images from build directory
- Removed per Product content directories
- default version to 0

* Wed Jun 27 2007 Jeff Fearn <jfearn@redhat.com> 0.15
- remove id from list-labels in questions & answers (duplicate id bug) 
- Fixed bogus publish path for Reports

* Wed Jun 27 2007 Jeff Fearn <jfearn@redhat.com> 0.14
- Added test-all target
- Disabled Hyphenation in FOP, zh PDFs hanging service

* Tue Jun 26 2007 Joshua Wulf <jwulf@redhat.com> 0.13
- Added JBEAP and JBEAPVER entities
- Optimised spec file creation

* Mon Jun 25 2007 Jeff Fearn <jfearn@redhat.com> 0.12
- Fix css rule that broke links

* Tue May 08 2007 Jeff Fearn <jfearn@redhat.com> 0.11
- add DocBook 4.5 DTD to package
- add DocBook 1.72.0 xsl to package
- modify makefiles to use new DocBook catalogs
- xmlClean:
-         Changed DTD from 4.3 to 4.5
-         Added bookname to node id's to help avoid id clashes in sets
-         Fixed line wrap issue in PDF generation for zh-CN and zh-TW
-         Enforced validation of xml on all build targets
-         Add legalnotice tag 
-         Add address tag 
-         Add street tag 
-         Add city tag 
-         Add state tag 
-         Add postcode tag 
-         Add country tag 
-         Add phone tag 
-         Add fax tag 
-         Add pob tag 
-         Add preface tag 
-         Add bibliograpy related tags 
-         Add qandaset related tags 
- Removed Confidential image and restyle confidential html text
- Added po2xlf script
- Added xlf2po script
- Added perl-XML-SimpleObject to Requires, used in xliff code
- Fixed Makefile.GUI updating po file for source lang
- Updated custom xml to match 1.72 docbook xsl
- Removed MuktiNarrow fonts - using lohit-bn
- Removed ZYSong18030 & ARPLSungtiLGB fonts - unused
- Modified Publish output line in logfile to be a URL
- Fixed creation of translated srpm
- Added Liberation fonts for PDF
- Removed DejaVuLGCSans fonts
- Turned on Line Wrap for monospace verbatim elements
- Moved entity SELinux from Translatable to Entities.ent, updated po files
- Added Legal_Notice to common
- Moved balance of non-translatable entities out of Translatable-entities.ent, updated po files
- Added missing Req perl-SGML-Translate, used for translation reports
- Updated documentation descriptions of Book_Info.xml tags. BZ #456489 BZ #456488


* Tue May 01 2007 Jeff Fearn <jfearn@redhat.com> 0.10
- fix image dimensions on content/common/en-US/images/redhat-logo.svg
- remove leading space from rpm spec desription
- Made abstract wrap at 72 characters and be left aligned.
-   it's used for the spec description
- Move legal notice link param from xhtml.xsl to main-html so nochunks
-   target will have legal notice embedded in page

* Tue Apr 24 2007 Jeff Fearn <jfearn@redhat.com> 0.9.1
- fix path to xsl <blush>

* Tue Apr 24 2007 Jeff Fearn <jfearn@redhat.com> 0.9
- Fix "Use of uninitialized value in string eq at xmlClean line 272."
- Add facility to prune xml tree based on condition attribute.
- Made COMMON_CONTENT static 

* Tue Apr 17 2007 Jeff Fearn <jfearn@redhat.com> 0.8
- fix non RHEL books not having the PRODUCT name attached to the
-  rpm and specfile to avoid duplicate name problems.
-  e.g. everyone has a Deployment_Guide so non RHEL books must be Fortitude-Deployment_Guide etc.

* Tue Apr 17 2007 Jeff Fearn <jfearn@redhat.com> 0.7
- format temporary fo file as the lines where to long and confused FOP ... grrr
- fixed po files not having links updated when clean_ids is run

* Tue Apr 17 2007 Jeff Fearn <jfearn@redhat.com> 0.6
- fix Book entity file being ignored
- add white space to TOC

* Tue Apr 17 2007 Jeff Fearn <jfearn@redhat.com> 0.5
- Revert to kdesdk (xml2pot) to fix RHEL4 bug where entities would be dropped from pot file.
- Switching to gnome-docs-util creates ~1500 hours of translation work in the
- Deployment Guide alone making the switch impossible at this time :(
- This means inline xml comments will break translation due to a bug in the sdk.
- Added the 4 scripts from doc-tools to bin/* to avoid adding deps.
- Added missing PRODUCT en-US & pot dirs

* Mon Apr 16 2007 Jeff Fearn <jfearn@redhat.com> 0.4
- Fix fop config file
- Roll back font metrics file to fop 0.2 format

* Mon Apr 16 2007 Jeff Fearn <jfearn@redhat.com> 0.3
- Fix xmlClean, clean_ids was note validating xref ids correctly

* Thu Apr 12 2007 Jeff Fearn <jfearn@redhat.com> 0.2
- Fix SYSTEM not being copied to PRODUCT properly
- Fix GUI Strings reports
- Fix GUI Strings css path
- Fix Set targets as per timp@redhat.com fix.

* Wed Apr 11 2007 Jeff Fearn <jfearn@redhat.com> 0.1.19
- Change SYSTEM to PRODUCT as it more clearly defines what it's used for.
- Add content to README
- Fix 'make help' output for Books

* Tue Apr 10 2007 Jeff Fearn <jfearn@redhat.com> 0.1.18
- Fix missing Entity file
- Remove graphic from boilerplate
- Fix fop metric path to meet new package path
- PDF Appendix, URL and title fixes

* Mon Apr 02 2007 Jeff Fearn <jfearn@redhat.com> 0.1.15
- add 'a' to start of ID's that begin with numbers.
- stop DTD entity strings being written in clean_id mode
- fix pdf formatting issues
- Merge Common_Config
- add missing Requirements
- add DejaVuLGCSans for Russian books

* Tue Mar 27 2007 Jeff Fearn <jfearn@redhat.com> 0.1.13
- add appendix and appendix info to xmlClean
- convert all configuration files from fop 0.20.5 to 0.93.0 format.
- remove copying of common configuration directory

* Mon Mar 26 2007 Jeff Fearn <jfearn@redhat.com> 0.1.12
- bump rev for brew build

* Fri Mar 23 2007 Jeff Fearn <jfearn@redhat.com> 0.1.11
- fixed use of dist

* Thu Mar 22 2007 Jeff Fearn <jfearn@redhat.com> 0.1.10
- Switch to using gnome-doc-utils for po manipulation

* Wed Mar 21 2007 Jeff Fearn <jfearn@redhat.com> 0.1.9
- Remove trailing space from text nodes in xmlClean
- add feed back for user

* Tue Mar 20 2007 Jeff Fearn <jfearn@redhat.com> 0.1.8
- Fix re-creation of $cmd variable
- Add support for per arch build

* Mon Mar 19 2007 Jeff Fearn <jfearn@redhat.com> 0.1.6
- Fix path for reports script

* Wed Feb 07 2007 Jeff Fearn <jfearn@redhat.com> 0.0
- Initial creation




