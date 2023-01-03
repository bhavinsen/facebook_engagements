from orator.migrations import Migration


class CreateFbEngagementsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('fb_engagements') as table:
            table.increments('id')
            table.integer('account_id').unsigned()
            table.foreign('account_id').references('id').on('facebook_accounts')
            table.integer('likes')	
            table.integer('shares')
            table.text('comments')	
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('fb_engagements')
