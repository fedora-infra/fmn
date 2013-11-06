<%inherit file="master.mak"/>
<div class="row">
  <div class="col-md-4">
    <p>Fedora Notifications is a family of systems built to manage end-user
    notifications triggered by <a href="http://fedmsg.com">fedmsg</a>, the
    Fedora FEDerated MESsage bus.</p>

    <p>The wins here are:

    <ul>
      <li>Diverse kinds of notification media.  Some users don't want email.
      </li>
      <li>A single place for end-users to manage notification preferences.
      Instead of having to tweak preferences in bodhi, koji, pkgdb, etc..  they
      can choose what they do and don't want to receive right here.  </li>
      <li>A single place for email code to live, instead of being duplicated in
      every application that we write and deploy.  This will ostensibly reduce
      the amount of code that the infrastructure team has to maintain.</li>
    </ul>
    </p>

    <p>We can currently serve notifications via these means:
      <dl class="dl-horizontal">
      % for ctx in contexts:
        <dt><a href="${ctx.name}">${ctx.name}</a></dt>
        <dd>${ctx.description}</dd>
      % endfor
      </dl>
    </p>

    <p><a href="${url_for('login')}">Log in</a> to check it out and set up your
      profile</p>

  </div>
  <div class="col-md-8">
    <img class="centered" src="/static/img/logo.png" />
  </div>
</div>
