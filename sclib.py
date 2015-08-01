#! /usr/bin/env python
"""
Sclib
"""
# Requere
# > pymongo
# > beautifulsoup4
# > scholar.py https://github.com/ckreibich/scholar.py



# TODO: 
# > create collections (TESIS, SCHOOL, ETC) with others arguments 
# > Finish the first version.

import argparse as arg
import sys, os
import pymongo as pm

#import datetime
#import shutil  
class Error(Exception):
    """Base class for any Sclib error."""


class ArgumentError(Error):
    """Argument error"""


PROG = 'sclib'
VERSION = '0.3'
LOG_LEVEL = 1


def Add(db,args):
    vprint(4,">>>> Add inicialization... \n")
    db.authenticate('writer','writer')
    import scholar

    biblio = db['default'] #select default collection


    db.logout()
    return 1

def Remove(args):
    vprint(4,">>>> Remove inicialization... \n")
    return 1



def Search(db,args):
    vprint(4,">>>> Search inicialization... \n")
    return 1


def OnlineSearch(db,args):
    vprint(4,">>>> Online search inicialization... \n")
    
#    def PrintWebSearch(v,querier):

    
    import scholar
    querier = scholar.ScholarQuerier()
    settings = scholar.ScholarSettings()

    citform = {'bt':scholar.ScholarSettings.CITFORM_BIBTEX,'en':scholar.ScholarSettings.CITFORM_ENDNOTE,'rw':scholar.ScholarSettings.CITFORM_REFWORKS,'rm':scholar.ScholarSettings.CITFORM_REFMAN}

    if args.citation != None :
        settings.set_citation_format(citform[args.citation])
    
    querier.apply_settings(settings)

    query = scholar.SearchScholarQuery()
    if args.author != None :
        query.set_author(' '.join(args.author))
    if args.all != None :
        query.set_words(' '.join(args.all))
    if args.some != None :
        query.set_words_some(' '.join(args.some))
    if args.none != None :
        query.set_words_none(' '.join(args.none))
    if args.since or args.until :
        query.set_timeframe(args.since,args.until)
    if not args.include_citations:
        query.set_include_citations(False)
    query.set_include_patents(False)
    args.max_results = min(args.max_results, scholar.ScholarConf.MAX_PAGE_RESULTS)
    query.set_num_page_results(args.max_results)

    querier.send_query(query)
    if args.citation != None :
        scholar.citation_export(querier)
    else :
        scholar.txt(querier,with_globals=True)
    return 1

def Tag(args):
    vprint(4,">>>> Tag inicialization... \n")
    return 1

def Open(args):
    vprint(4,">>>> Open inicialization... \n")
    return 1

def Meta(args):
    vprint(4,">>>> Meta inicialization... \n")
    import scholar
    return 1

def Export(args):
    vprint(4,">>>> Export inicialization... \n")
    return 1

def Config(db,args):
    DEF_VIEW = '/usr/bin/okular'
    DEF_EDITOR = '/usr/bin/vim'
    DEF_BASEPATH = '~/'+PROG
    vprint(4,">>>> Config inicialization... \n")

    if args.install:
        if args.set_viewer != None :
            DEF_VIEW = args.set_viewer
        if args.set_editor != None :
            DEF_EDITOR = args.set_editor
        if args.set_basepath != None :
            DEF_BASEPATH = args.set_basepath
        vprint(0,
    """
    =========================
       Welcome to %s !
    =========================
    > Creating users...""",PROG)
        db.add_user('ronly','ronly',read_only=True)
        db.add_user('writer','writer')
        vprint(0,"Ok! \n> Creating collections...\n")
            
        vprint(0,">> Setting the default config:\n>>> Editor: %s\n>>> Viewer: %s\n>>> Basepath: %s\n" % (DEF_EDITOR,DEF_VIEW,DEF_BASEPATH))
        conf = db['config']
        try :
            class ViewerError(Error):
                """Viewer error"""
            class EditorError(Error):
                """Editor error"""

            if not os.path.isfile(DEF_VIEW) :
                raise ViewerError
            if not os.path.isfile(DEF_EDITOR):
                raise EditorError
            try :
                if DEF_BASEPATH[-1] is not '/':
                    DEF_BASEPATH += '/'
                DIR = os.path.dirname(os.path.expanduser(DEF_BASEPATH))
                os.makedirs(DIR)
            except OSError :
                pass
            conf.insert_one({"_id":'viewer',
                "name":DEF_VIEW,
                "old_name":""})

            conf.insert_one({"_id":'editor',
                "name":DEF_EDITOR,
                "old_name":""})
            
            conf.insert_one({"_id":'basepath',
                "name":DEF_BASEPATH,
                "old_name":""})
            conf.insert_one({"_id":'default_collection',
                "name":"default",
                "old_name":""})
        except pm.errors.DuplicateKeyError:
            sys.stderr.write("\nerror: There is another installation of %s (PrimaryKey duplication). Please uninstall it before the new installation\n" % PROG)
            sys.stderr.flush()
            sys.exit(1)
        except ViewerError:
            sys.stderr.write("error: The viewer: %s doesn't exist\n" % DEF_VIEW)
            sys.stderr.write("       please use --set-viewer to set a valid viewer\n")
            sys.stderr.flush()
            sys.exit(1)
        except EditorError:
            sys.stderr.write("error: The editor: %s doesn't exist\n" % DEF_EDITOR)
            sys.stderr.write("       please use --set-editor to set a valid editor\n")
            sys.stderr.flush()
            sys.exit(1)

        vprint(0,">> Ok!\n") # def conf
        vprint(0,"> Ok!\n\n")  # collections
        vprint(0,"> Installation complete !\n")
        return 1

    if args.set_viewer != None :
        try :
            if not os.path.isfile(args.set_viewer):
                raise ArgumentError
            db.authenticate('writer','writer')
            conf = db['config']
            old_name = conf.find_one({"_id":"viewer"})['name']
            vprint(1,">> changing viewer from %s to %s\n" % (old_name,args.set_viewer))
            conf.update({'_id':"viewer"},
                    {"name":args.set_viewer,
                        'old_name':old_name})
            db.logout()

        except ArgumentrError:
            sys.stderr.write("error: The viewer: %s doesn't exist\n" % args.set_viewer)
            sys.stderr.write("       please use --set-viewer to set a valid viewer\n")
            sys.stderr.flush()
            sys.exit(1)


    if args.set_editor != None :
        try :
            if not os.path.isfile(args.set_editor):
                raise ArgumentError
            db.authenticate('writer','writer')
            conf = db['config']
            old_name = conf.find_one({"_id":"editor"})['name']
            vprint(1,">> changing editor from %s to %s\n" % (old_name,args.set_editor))
            conf.update({'_id':"editor"},
                    {"name":args.set_editor,
                        'old_name':old_name})
            db.logout()

        except ArgumentError:
            sys.stderr.write("error: The editor: %s doesn't exist\n" % args.set_editor)
            sys.stderr.write("       please use --set-editor to set a valid editor\n")
            sys.stderr.flush()
            sys.exit(1)



    if args.set_basepath != None :
        try :
            if not os.path.isdir(args.set_basepath):
                if args.set_basepath[-1] is not '/':
                     args.set_basepath+= '/'
                DIR = os.path.dirname(os.path.expanduser(args.set_basepath))
                os.makedirs(DIR)
            db.authenticate('writer','writer')
            conf = db['config']
            old_name = conf.find_one({"_id":"basepath"})['name']
            vprint(1,">> changing basepath from %s to %s\n" % (old_name,args.set_basepath))
            conf.update({'_id':"basepath"},
                    {"name":args.set_basepath,
                        'old_name':old_name})
            db.logout()

        except OSError :
            sys.stderr.write("error: %s doesn't have permission to write %s \n" % (PROG,args.set_basepath))
            sys.stderr.flush()
            sys.exit(1)

    if args.uninstall:
        vprint(0,"Are you sure that you want to uninstall %s ? [y/N]" % PROG)
        try : #python 3.x
            answer = input()[0]
        except : #python 2.x
            answer = raw_input()
            
        if answer in ['y','Y']:
            vprint(0,"UNINSTALLING !\n")
            return 1
        return 0
    if args.default:
        db.authenticate('ronly','ronly')
        conf = db['config']
        viewer = conf.find_one({'_id':'viewer'})['name']
        editor = conf.find_one({'_id':'editor'})['name']
        basepath = conf.find_one({'_id':'basepath'})['name']
        vprint(0,"%10s: %s\n" % ("viewer",viewer))
        vprint(0,"%10s: %s\n" % ("editor",editor))
        vprint(0,"%10s: %s\n" % ("basepath",basepath))
        db.logout()



    if args.restore != None :
        db.authenticate('writer','writer')
        conf = db['config']
        if args.restore == 'all':
            restore = ['viewer','editor','basepath']
        else :
            restore = list(args.restore)
        for entry in restore:
            try :
                old_name = conf.find_one({"_id":entry})['old_name']
                name = conf.find_one({"_id":entry})['name']
                if not os.path.isfile(old_name) or (os.path.isdir(old_name) and entry == 'basepath'):
                    if old_name == '': old_name ="(null)"
                    raise FileArgError
                vprint(1,">> restoring basepath from %s to %s\n" % (name,old_name))
                conf.update({'_id':entry},
                        {"name":old_name,
                            'old_name':name})
            except ArgumentError:
                vprint(0,"> ignoring argument (file or directory doesn't exist): %s(%s)\n"%(old_name,entry))
        db.logout()
        

    return 1


def main():
    argparser = arg.ArgumentParser(description="Sclib library",prog=PROG)
    argparser.add_argument('--verbose', '-v', action='count')
    argparser.add_argument('--debug',help="'debug' mode",action='store_true')
    subparser = argparser.add_subparsers(help='subcommand help')

	
    Add_parser = subparser.add_parser('add',help='add new entry to %(prog)s')
    Add_parser.set_defaults(routine='add')
    Add_parser.add_argument('--file','-f', help='set file path',nargs='?')
    Add_parser.add_argument('--author','-a', help='set author',nargs='*')
    Add_parser.add_argument('--title','-t', help='set title',nargs='?')
    Add_parser.add_argument('--year','-y', help='set year',nargs='?')
    Add_parser.add_argument('--journal','-j', help='set journal',nargs='?')
    Add_parser.add_argument('--tag', help='set tag',nargs='*')
    Add_parser.add_argument('--review','-r', help='add and open review', action='store_true')
    Add_parser.add_argument('--offline', help='dont search metadata on cloud (GoogleScholar)',action='store_true')

    Remove_parser = subparser.add_parser('remove',help='remove entry from %(prog)s')
    Remove_parser.set_defaults(routine='remove')
    Remove_parser.add_argument('id',metavar='ID',nargs='*')
    Remove_parser.add_argument('--interactive','-i', help='interactive mode',action='store_true')

    Tag_parser = subparser.add_parser('tag',help='tag/untag')
    Tag_parser.set_defaults(routine='tag')
    Tag_parser.add_argument('id', help='set id to tag/untag',nargs='*')
    Tag_parser.add_argument('--add','-a', help='add tag to id',nargs='*',metavar='TAG')
    Tag_parser.add_argument('--remove','-r', help='remove tag from id',nargs='*',metavar='TAG')
    
    Search_parser = subparser.add_parser('search',description="Search inside %s database" % PROG,help='search by author/title/year/journal/tag')
    Search_parser.set_defaults(routine='search')
    Search_parser = Search_parser.add_argument_group()
    Search_parser.add_argument('--id','-i', help='search id',nargs='*')
    Search_parser.add_argument('--author','-A', help='filter by author',nargs='*')
    Search_parser.add_argument('--title','-t', help='filter by title',nargs='*')
    Search_parser.add_argument('--year','-y', help='filter by year',nargs='*')
    Search_parser.add_argument('--journal','-j', help='filter by journal',nargs='*')
    Search_parser.add_argument('--tag', help='filter by tag',nargs='*')
    
    
    OSearch_parser = subparser.add_parser('websearch',help='search online (GoogleScholar)')
    OSearch_parser.set_defaults(routine='osearch')
    OSearch_parser.add_argument('--author','-a', help='filter by author',nargs='*')
    OSearch_parser.add_argument('--some','-S', help='results must contain some of this words',nargs='*',metavar='WORD')
    OSearch_parser.add_argument('--all','-A', help='results must contain all of this words',nargs='*',metavar='WORD')
    OSearch_parser.add_argument('--none','-NN', help='results must contain none of this words',nargs='*',metavar='WORD')
    OSearch_parser.add_argument('--since','-s', help='filter by years (since)',metavar='YEAR',type=int)
    OSearch_parser.add_argument('--until','-u', help='filter by years (until)',metavar='YEAR',type=int)
    OSearch_parser.add_argument('--max-results','-mr', help='maximum number of results',metavar='NUMBER',type=int,default=20)
    OSearch_parser.add_argument('--citation','-cit', help='citation scheme: BibTeX(bt), EndNote(en) RefWorks(rw) RefMan(rm)',choices=['bt','en','rw','rm'])
    OSearch_parser.add_argument('--include-citations','-icit', help='include citation number',action='store_true')

    Open_parser = subparser.add_parser('open',help='open file/review/over-review')
    Open_parser.set_defaults(routine='open')
    Open_parser.add_argument('id',metavar='ID/TAG')
    Open_parser.add_argument('--show','-s', help='open the file [ID]',action='store_true')
    Open_parser.add_argument('--review','-r', help='open the review file [ID]',action='store_true')
    Open_parser.add_argument('--over-review','-or', help='open the overreview file [TAGS]',action='store_true')
    
    Meta_parser = subparser.add_parser('metadata',help='edit metadata')
    Meta_parser.set_defaults(routine='meta')
    Meta_parser.add_argument('id',metavar='ID')
    Meta_parser.add_argument('--manual','-m', help='update metadata manualy (default=false)',action='store_true')
    
    Export_parser = subparser.add_parser('export',help='export files/references')
    Export_parser.set_defaults(routine='export')
    Export_parser.add_argument('--path','-p', help='set the path were export',nargs='?')
    Export_parser.add_argument('--id','-i', help='export by id',nargs='*')
    Export_parser.add_argument('--author','-a', help='export by author',nargs='*')
    Export_parser.add_argument('--journal','-j', help='export by journal',nargs='*')
    Export_parser.add_argument('--year','-y', help='export by year',nargs='*')
    Export_parser.add_argument('--tag','-t', help='export by tag',nargs='*')
    Export_parser.add_argument('--gzip','-gz', help='compress the exported files',action='store_true')
    Export_parser.add_argument('--bibtex','-bt', help='export bibtex',action='store_true')
    Export_parser.add_argument('--endnote','-en', help='export endnote',action='store_true')
    Export_parser.add_argument('--refworks','-rw', help='export refworks',action='store_true')
    Export_parser.add_argument('--refman','-rm', help='export refman',action='store_true')
    
    Config_parser = subparser.add_parser('config',help='set configuration of %(prog)s')
    Config_parser.set_defaults(routine='config')
    Config_parser.add_argument('--default', help='show default config',action='store_true')
    Config_parser.add_argument('--set-viewer', help='set default viewer',nargs='?',metavar='VIEWER')
    Config_parser.add_argument('--set-editor', help='set default editor',nargs='?',metavar='EDITOR')
    Config_parser.add_argument('--set-basepath', help='set default basepath of %(prog)s',nargs='?',metavar='PATH')
    Config_group = Config_parser.add_mutually_exclusive_group()
    Config_group.add_argument('--restore',nargs='+',choices=['all','viewer','editor','basepath'],help="Restore to last configuration")
    Config_group.add_argument('--install',action='store_true',help="Installation of %(prog)s")
    Config_group.add_argument('--uninstall',action='store_true',help="Uninstallation of %(prog)s")

    args = argparser.parse_args()

    if args.debug: 
        args.verbose = 4
    if args.verbose:
        def _vprint(*argv):
            #usage: vprint( msg_lvl, msg)
            if argv[0] <= args.verbose:
                sys.stdout.write(argv[1])
                sys.stdout.flush()
    else :
        _vprint = lambda *a: None
    global vprint
    vprint = _vprint


    routines = {'none':0,'add':Add,'remove':Remove,'search':Search,'osearch':OnlineSearch,'tag':Tag,'open':Open,'meta':Meta,'export':Export,'config':Config}
    vprint(4,">>>> arguments: %s \n" % args)
    try : 
        client = pm.MongoClient('localhost', 27017)
        client.server_info()
        vprint(4,">>>> connection set on %s \n" % (client))
        db = client[PROG]
        db.authenticate('ronly','ronly')
        db.logout()
        vprint(4,">>>> connection to database successfull\n")
    except pm.errors.ConnectionFailure:
        sys.stderr.write("error: couldn't connect to mongodb (timeout) \n" )
        sys.stderr.flush()
        sys.exit(1)
    except pm.errors.OperationFailure:
        if not (args.routine == 'config' and args.install):
            vprint(0,"> First time running %s ? please run:\n\t %s %s\n" % (PROG,PROG,'config --install'))
            sys.exit(1)


    vprint(4,">>>> %s %s routine... \n" % (PROG,args.routine))
    routines[args.routine](db,args)

if __name__ == "__main__":
    sys.exit(main())
