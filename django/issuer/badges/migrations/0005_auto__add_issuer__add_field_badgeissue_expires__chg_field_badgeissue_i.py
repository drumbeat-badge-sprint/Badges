# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Issuer'
        db.create_table('badges_issuer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('badges', ['Issuer'])

        # Adding M2M table for field users on 'Issuer'
        db.create_table('badges_issuer_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issuer', models.ForeignKey(orm['badges.issuer'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('badges_issuer_users', ['issuer_id', 'user_id'])

        # Adding field 'BadgeIssue.expires'
        db.add_column('badges_badgeissue', 'expires', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2100, 12, 31, 0, 0)), keep_default=False)

        # Renaming column for 'BadgeIssue.issuer' to match new field type.
        db.rename_column('badges_badgeissue', 'issuer', 'issuer_id')
        # Changing field 'BadgeIssue.issuer'
        db.alter_column('badges_badgeissue', 'issuer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Issuer']))

        # Adding index on 'BadgeIssue', fields ['issuer']
        db.create_index('badges_badgeissue', ['issuer_id'])

        # Adding field 'Badge.image'
        db.add_column('badges_badge', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Badge.imageURL'
        db.add_column('badges_badge', 'imageURL', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Removing index on 'BadgeIssue', fields ['issuer']
        db.delete_index('badges_badgeissue', ['issuer_id'])

        # Deleting model 'Issuer'
        db.delete_table('badges_issuer')

        # Removing M2M table for field users on 'Issuer'
        db.delete_table('badges_issuer_users')

        # Deleting field 'BadgeIssue.expires'
        db.delete_column('badges_badgeissue', 'expires')

        # Renaming column for 'BadgeIssue.issuer' to match new field type.
        db.rename_column('badges_badgeissue', 'issuer_id', 'issuer')
        # Changing field 'BadgeIssue.issuer'
        db.alter_column('badges_badgeissue', 'issuer', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Deleting field 'Badge.image'
        db.delete_column('badges_badge', 'image')

        # Deleting field 'Badge.imageURL'
        db.delete_column('badges_badge', 'imageURL')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'badges.badge': {
            'Meta': {'object_name': 'Badge'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'imageURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '125'})
        },
        'badges.badgeclaim': {
            'Meta': {'object_name': 'BadgeClaim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'claims'", 'to': "orm['badges.BadgeIssue']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'badges.badgeissue': {
            'Meta': {'object_name': 'BadgeIssue'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues'", 'to': "orm['badges.Badge']"}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2100, 12, 31, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues'", 'to': "orm['badges.Issuer']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues'", 'to': "orm['auth.User']"})
        },
        'badges.issuer': {
            'Meta': {'object_name': 'Issuer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'issuers'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['badges']
